from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


DEFAULT_KEYWORDS: List[str] = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Engineer",
    "Software Engineer",
    "Full Stack Engineer",
]


@dataclass
class AppConfig:
    source: str = "linkedin"
    keyword: str = "AI Engineer"
    location: str = "Singapore"
    max_jobs: int = 25
    output_dir: str = "outputs"
    proxy: str = ""
    request_timeout: int = 20
    rate_limit_seconds: float = 4.0
    keywords: List[str] = field(default_factory=lambda: list(DEFAULT_KEYWORDS))
    demo_mode: bool = False

    @classmethod
    def from_args(cls, args: object) -> "AppConfig":
        config = cls(
            source=getattr(args, "source", "linkedin") or "linkedin",
            keyword=getattr(args, "keyword", "AI Engineer") or "AI Engineer",
            location=getattr(args, "location", "Singapore") or "Singapore",
            max_jobs=max(1, int(getattr(args, "max_jobs", 25) or 25)),
            output_dir=getattr(args, "output_dir", "outputs") or "outputs",
            proxy=getattr(args, "proxy", "") or "",
            request_timeout=int(getattr(args, "request_timeout", 20) or 20),
            rate_limit_seconds=float(getattr(args, "rate_limit_seconds", 4.0) or 4.0),
            demo_mode=bool(getattr(args, "demo", False)),
        )
        config.keywords = [
            value.strip()
            for value in (os.getenv("KEYWORDS", "").split(",") if os.getenv("KEYWORDS") else [])
            if value.strip()
        ] or [config.keyword]
        return config


def load_environment_config() -> AppConfig:
    return AppConfig(
        source=os.getenv("SOURCE", "linkedin"),
        keyword=os.getenv("KEYWORD", "AI Engineer"),
        location=os.getenv("LOCATION", "Singapore"),
        max_jobs=int(os.getenv("MAX_JOBS", "25")),
        output_dir=os.getenv("OUTPUT_DIR", "outputs"),
        proxy=os.getenv("PROXY_URL", "").strip(),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "20")),
        rate_limit_seconds=float(os.getenv("RATE_LIMIT_SECONDS", "4.0")),
        keywords=[
            kw.strip() for kw in os.getenv("KEYWORDS", "").split(",") if kw.strip()
        ] or [os.getenv("KEYWORD", "AI Engineer")],
    )
