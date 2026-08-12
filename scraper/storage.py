import csv
import json
from pathlib import Path
from typing import Iterable, List

from .models import JobRecord


def ensure_output_dir(path: str) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def write_csv(jobs: Iterable[JobRecord], output_dir: str) -> Path:
    directory = ensure_output_dir(output_dir)
    path = directory / "jobs.csv"
    fieldnames = [
        "job_title",
        "company",
        "location",
        "description_snippet",
        "posted_date",
        "url",
        "source",
        "scraped_at",
    ]
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for record in jobs:
            writer.writerow(record.to_dict())
    return path


def write_json(jobs: Iterable[JobRecord], output_dir: str) -> Path:
    directory = ensure_output_dir(output_dir)
    path = directory / "jobs.json"
    payload = [job.to_dict() for job in jobs]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_jsonl(jobs: Iterable[JobRecord], output_dir: str) -> Path:
    directory = ensure_output_dir(output_dir)
    path = directory / "jobs.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for record in jobs:
            handle.write(json.dumps(record.to_dict(), ensure_ascii=False))
            handle.write("\n")
    return path


def write_outputs(jobs: List[JobRecord], output_dir: str) -> dict[str, Path]:
    return {
        "csv": write_csv(jobs, output_dir),
        "json": write_json(jobs, output_dir),
        "jsonl": write_jsonl(jobs, output_dir),
    }
