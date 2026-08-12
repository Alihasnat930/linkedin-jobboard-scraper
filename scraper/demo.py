from __future__ import annotations

from .cleaners import dedupe_jobs
from .models import JobRecord


def build_demo_jobs(keyword: str = "AI Engineer", location: str = "Singapore", max_jobs: int = 25) -> list[JobRecord]:
    titles = [
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Engineer",
        "Full Stack Engineer",
        "Platform Engineer",
        "Applied Scientist",
    ]
    companies = [
        "Northstar AI",
        "Apex Robotics",
        "Signal Forge",
        "Glacier Labs",
        "Sphere Digital",
        "Velora Systems",
        "Finora Tech",
    ]
    jobs: list[JobRecord] = []
    for index in range(min(max_jobs, 12)):
        title = titles[index % len(titles)]
        company = companies[index % len(companies)]
        jobs.append(
            JobRecord(
                job_title=title,
                company=company,
                location=location or "Singapore",
                description_snippet=(
                    "Design and ship AI features, build model pipelines, and collaborate with cross-functional teams "
                    "in a product-focused environment."
                ),
                posted_date="1 day ago",
                url=f"https://www.linkedin.com/jobs/view/{3000 + index}",
                source="linkedin-demo",
            )
        )
    return dedupe_jobs(jobs)
