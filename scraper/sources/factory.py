from __future__ import annotations

from ..config import AppConfig
from .linkedin import LinkedInAdapter


def get_source_adapter(source_name: str, config: AppConfig):
    source_name = (source_name or "linkedin").strip().lower()
    if source_name == "linkedin":
        return LinkedInAdapter(config)
    raise ValueError(f"Unsupported source: {source_name}")
