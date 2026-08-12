from scraper.cleaners import clean_text, dedupe_jobs, normalize_location
from scraper.demo import build_demo_jobs
from scraper.models import JobRecord


def test_clean_text_removes_extra_whitespace():
    assert clean_text("  AI   Engineer  ") == "AI Engineer"


def test_normalize_location_handles_singapore():
    assert normalize_location("Singapore, SG") == "Singapore"
    assert normalize_location("Remote") == "Remote"


def test_dedupe_jobs_removes_duplicates():
    a = JobRecord(
        job_title="AI Engineer",
        company="Pioneer AI",
        location="Singapore",
        description_snippet="Build AI systems",
        posted_date="1 day ago",
        url="https://example.com/1",
        source="linkedin",
    )
    b = JobRecord(
        job_title="AI Engineer",
        company="Pioneer AI",
        location="Singapore",
        description_snippet="Build AI systems",
        posted_date="1 day ago",
        url="https://example.com/1",
        source="linkedin",
    )
    assert len(dedupe_jobs([a, b])) == 1


def test_demo_jobs_include_required_fields():
    jobs = build_demo_jobs(max_jobs=5)
    assert len(jobs) == 5
    for job in jobs:
        assert job.job_title
        assert job.company
        assert job.location
        assert job.url
        assert job.source
