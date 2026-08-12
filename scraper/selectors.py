"""Centralized selectors for job-board adapters.

This keeps scraping logic readable and makes it easy to swap provider-specific selectors
without changing the rest of the project.
"""

LINKEDIN_SELECTORS = {
    "job_cards": "li.jobs-search-results__list-item",
    "job_title": "h3.base-search-card__title",
    "company": ".job-search-card__company-name, .base-search-card__subtitle",
    "location": ".job-search-card__location, .base-search-card__metadata",
    "description": ".job-search-card__snippet, .base-search-card__snippet",
    "posted_date": ".job-search-card__date, .base-search-card__metadata",
    "job_link": "a[href*='/jobs/view/']",
}

SOURCE_SELECTORS = {
    "linkedin": LINKEDIN_SELECTORS,
    "jobstreet": {},
    "mycareersfuture": {},
    "naukri": {},
    "seek": {},
}
