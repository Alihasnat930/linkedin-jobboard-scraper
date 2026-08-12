from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ..config import AppConfig
from ..models import JobRecord


class SourceAdapter(ABC):
    name = "base"

    def __init__(self, config: AppConfig):
        self.config = config

    @abstractmethod
    def scrape(self, keyword: str, location: str, max_jobs: int) -> List[JobRecord]:
        raise NotImplementedError
