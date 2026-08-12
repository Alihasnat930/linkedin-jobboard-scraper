import re
from datetime import datetime, timezone
from typing import Iterable, List

from .models import JobRecord


def clean_text(value: str, *, max_chars: int | None = None) -> str:
    if value is None:
        return ""
    cleaned = re.sub(r"\s+", " ", str(value).replace("\xa0", " ")).strip()
    if max_chars and len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars].strip()
    return cleaned


def normalize_location(value: str, fallback: str = "Singapore") -> str:
    cleaned = clean_text(value)
    if not cleaned:
        return fallback
    if "singapore" in cleaned.lower():
        return "Singapore"
    if "remote" in cleaned.lower():
        return "Remote"
    return cleaned


def normalize_url(value: str) -> str:
    cleaned = clean_text(value)
    if not cleaned:
        return ""
    if cleaned.startswith("//"):
        return "https:" + cleaned
    return cleaned


def normalize_posted_date(value: str) -> str:
    cleaned = clean_text(value)
    if not cleaned:
        return "Unknown"
    return cleaned


def dedupe_jobs(jobs: Iterable[JobRecord]) -> List[JobRecord]:
    seen: set[tuple[str, str, str]] = set()
    unique: List[JobRecord] = []
    for job in jobs:
        job.job_title = clean_text(job.job_title)
        job.company = clean_text(job.company)
        job.location = normalize_location(job.location)
        job.description_snippet = clean_text(job.description_snippet, max_chars=500)
        job.posted_date = normalize_posted_date(job.posted_date)
        job.url = normalize_url(job.url)
        key = (
            (job.url or "").lower(),
            (job.job_title or "").lower(),
            (job.company or "").lower(),
        )
        if not key[0] and not key[1] and not key[2]:
            continue
        if key in seen:
            continue
        seen.add(key)
        unique.append(job)
    return unique


def fresh_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
