from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class JobRecord:
    job_title: str = ""
    company: str = ""
    location: str = ""
    description_snippet: str = ""
    posted_date: str = ""
    url: str = ""
    source: str = "linkedin"
    scraped_at: str = ""

    def __post_init__(self) -> None:
        if not self.scraped_at:
            self.scraped_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
