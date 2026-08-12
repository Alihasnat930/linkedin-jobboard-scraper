from __future__ import annotations

import argparse

from scraper.cleaners import dedupe_jobs
from scraper.config import AppConfig
from scraper.demo import build_demo_jobs
from scraper.sources.factory import get_source_adapter
from scraper.storage import write_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Standalone LinkedIn and job-board scraper")
    parser.add_argument("--source", default="linkedin", help="Source adapter to use (currently: linkedin)")
    parser.add_argument("--keyword", default="AI Engineer", help="Job keyword to search for")
    parser.add_argument("--location", default="Singapore", help="Location filter, e.g. Singapore")
    parser.add_argument("--max-jobs", type=int, default=25, help="Maximum jobs to return")
    parser.add_argument("--output-dir", default="outputs", help="Directory for CSV/JSON/JSONL output")
    parser.add_argument("--proxy", default="", help="Optional proxy URL, e.g. http://127.0.0.1:8080")
    parser.add_argument("--request-timeout", type=int, default=20, help="HTTP timeout in seconds")
    parser.add_argument("--rate-limit-seconds", type=float, default=4.0, help="Minimum wait between requests")
    parser.add_argument("--demo", action="store_true", help="Generate sample output without live website access")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config = AppConfig.from_args(args)

    try:
        if config.demo_mode:
            jobs = build_demo_jobs(config.keyword, config.location, config.max_jobs)
        else:
            adapter = get_source_adapter(config.source, config)
            jobs = adapter.scrape(config.keyword, config.location, config.max_jobs)
    except Exception as exc:  # pragma: no cover - runtime guard for live scrapes
        print(f"Live scrape failed gracefully for source={config.source}: {exc}")
        jobs = []

    jobs = dedupe_jobs(jobs)[: config.max_jobs]
    output_paths = write_outputs(jobs, config.output_dir)

    if not jobs:
        print(f"No jobs returned for source={config.source} keyword={config.keyword!r} location={config.location!r}. Output files were still generated.")
    else:
        print(f"Scraped {len(jobs)} jobs for source={config.source} keyword={config.keyword!r} location={config.location!r}")
    for label, path in output_paths.items():
        print(f"{label.upper()}: {path}")


if __name__ == "__main__":
    main()
