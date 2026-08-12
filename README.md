# LinkedIn & Job Board Scraper

A standalone Python project for scraping public job listings with a clean source-adapter architecture. It is intentionally separated from the Nexus-CRM codebase and only includes reusable job-scraping functionality.

## What this project includes

- LinkedIn adapter for public job search pages
- Source adapter architecture for future sources (JobStreet, MyCareersFuture, Naukri, Seek)
- Singapore-first location filtering
- configurable keywords and max job limits
- deduplication and data cleaning
- retry/backoff and conservative throttling
- configurable proxy support
- CSV, JSON, and JSONL export
- demo mode with live-site-free sample output
- CLI runner with structured output

## Project goals

- Preserve the proven extraction logic pattern used in the existing CRM scraper: parse public search results, normalize URLs, dedupe results, and keep output structured.
- Remove CRM-specific workflow, database, and app code.
- Stay respectful: no CAPTCHA bypass, no login bypass, no access-control circumvention.

## Quick start

1. Create a local virtual environment and install dependencies:

   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Copy the example environment file:

   copy .env.example .env

3. Run a live scrape against LinkedIn (Singapore sample):

   python main.py --source linkedin --keyword "AI Engineer" --location Singapore --max-jobs 50

4. Run the demo output without live website access:

   python main.py --demo

## CLI usage

```bash
python main.py --source linkedin --keyword "AI Engineer" --location Singapore --max-jobs 50
python main.py --source linkedin --keyword "Data Engineer" --location "Singapore" --proxy "http://127.0.0.1:8080"
python main.py --demo
```

### Output files

The runner writes files to the `outputs/` directory:

- jobs.csv
- jobs.json
- jobs.jsonl

## Architecture

The project is organized in a reusable adapter style:

- `scraper/config.py` - CLI and environment configuration
- `scraper/selectors.py` - centralized selectors for supported sources
- `scraper/models.py` - structured job schema
- `scraper/cleaners.py` - location and text normalization
- `scraper/retry.py` - retry/backoff logic
- `scraper/rate_limiter.py` - conservative throttling
- `scraper/sources/base.py` - adapter contract
- `scraper/sources/linkedin.py` - LinkedIn source implementation
- `scraper/storage.py` - CSV/JSON/JSONL writing

The adapter pattern makes it straightforward to add JobStreet, MyCareersFuture, Naukri, and Seek later without reworking the CLI or output layer.

## Notes on scraper behavior

- Conservative rate limiting is enforced between requests.
- The scraper accepts optional proxy configuration through `PROXY_URL` or `--proxy`.
- Live scraping gracefully fails when LinkedIn is blocked or Playwright is not installed.
- Demo mode always works without internet access.

## Docker

```bash
docker build -t linkedin-job-scraper .
docker run --rm linkedin-job-scraper
```

## Testing

```bash
pytest
```

## Freelancer contest screenshot list

Capture the following screenshots:

1. Terminal showing `python main.py --demo`
2. Terminal showing `python main.py --source linkedin --keyword "AI Engineer" --location Singapore --max-jobs 50`
3. Generated `outputs/jobs.csv` preview
4. Generated `outputs/jobs.json` preview
5. Generated `outputs/jobs.jsonl` preview
6. README or project structure showing the clean standalone architecture
7. Docker build output or Dockerfile summary

## License

This project is provided for educational and contest use as a standalone job-scraping utility.
