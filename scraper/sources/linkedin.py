from __future__ import annotations

import re
from urllib.parse import quote

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - handled at runtime
    sync_playwright = None  # type: ignore[assignment]

from ..cleaners import clean_text, dedupe_jobs, normalize_location
from ..config import AppConfig
from ..models import JobRecord
from ..rate_limiter import RateLimiter
from ..retry import retry_with_backoff
from ..selectors import SOURCE_SELECTORS
from .base import SourceAdapter


class LinkedInAdapter(SourceAdapter):
    name = "linkedin"

    def __init__(self, config: AppConfig):
        super().__init__(config)
        self.selectors = SOURCE_SELECTORS["linkedin"]
        self.limiter = RateLimiter(config.rate_limit_seconds)

    @staticmethod
    def _demo_jobs(keyword: str, location: str, max_jobs: int) -> list[JobRecord]:
        sample_titles = [
            "AI Engineer",
            "Applied AI Engineer",
            "Data Engineer",
            "Machine Learning Engineer",
            "Senior Software Engineer",
        ]
        sample_companies = [
            "Apex Labs",
            "Nexora AI",
            "VisionWorks",
            "Vertex Commerce",
            "Helio Systems",
            "Northstar Analytics",
        ]
        jobs: list[JobRecord] = []
        for index in range(min(max_jobs, 10)):
            title = sample_titles[index % len(sample_titles)]
            company = sample_companies[index % len(sample_companies)]
            jobs.append(
                JobRecord(
                    job_title=title,
                    company=company,
                    location=location or "Singapore",
                    description_snippet=(
                        "Build production AI systems, design data pipelines, and ship robust services "
                        "for enterprise customers in Singapore."
                    ),
                    posted_date="2 days ago",
                    url=f"https://www.linkedin.com/jobs/view/{1000 + index}",
                    source="linkedin",
                )
            )
        return jobs

    @retry_with_backoff(max_retries=2, base_delay=1.0, backoff_factor=2.0)
    def scrape(self, keyword: str, location: str, max_jobs: int) -> list[JobRecord]:
        if self.config.demo_mode:
            return self._demo_jobs(keyword, location, max_jobs)
        if sync_playwright is None:
            raise RuntimeError(
                "Playwright is not installed. Run: pip install -r requirements.txt && python -m playwright install chromium"
            )

        query = quote(keyword)
        location_query = quote(location or self.config.location or "Singapore")
        url = (
            "https://www.linkedin.com/jobs/search/?keywords="
            f"{query}&location={location_query}&geoId=101659952&trk=public_jobs_jobs-search-bar_search-submit"
        )

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage"],
                )
                page = browser.new_page(viewport={"width": 1440, "height": 1600})
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=self.config.request_timeout * 1000)
                    page.wait_for_timeout(2000)
                    cards = page.locator(self.selectors["job_cards"]).all()
                finally:
                    browser.close()
        except Exception as exc:  # pragma: no cover - browser setup can vary by environment
            raise RuntimeError(
                "LinkedIn live scraping is unavailable. Ensure Playwright Chromium is installed with: "
                "python -m playwright install chromium. The scraper will fail gracefully rather than evading controls."
            ) from exc

        records: list[JobRecord] = []
        for card in cards[: max_jobs * 2]:
            self.limiter.wait()
            try:
                title = clean_text(card.locator(self.selectors["job_title"]).first.inner_text())
            except Exception:
                title = ""
            try:
                company = clean_text(card.locator(self.selectors["company"]).first.inner_text())
            except Exception:
                company = ""
            try:
                location_text = clean_text(card.locator(self.selectors["location"]).first.inner_text())
            except Exception:
                location_text = ""
            try:
                description = clean_text(card.locator(self.selectors["description"]).first.inner_text(), max_chars=500)
            except Exception:
                description = ""
            try:
                posted = clean_text(card.locator(self.selectors["posted_date"]).first.inner_text())
            except Exception:
                posted = ""
            try:
                link = card.locator(self.selectors["job_link"]).first.get_attribute("href")
            except Exception:
                link = ""

            if not title and not company and not link:
                continue

            records.append(
                JobRecord(
                    job_title=title,
                    company=company,
                    location=normalize_location(location_text, location or "Singapore"),
                    description_snippet=description,
                    posted_date=posted or "Unknown",
                    url=("https://www.linkedin.com" + link if link and link.startswith("/") else link),
                    source="linkedin",
                )
            )

        final_jobs = dedupe_jobs(records)[:max_jobs]
        return final_jobs
