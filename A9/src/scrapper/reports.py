from pydantic import BaseModel, ValidationError
from collections.abc import Callable
from pathlib import Path

__all__ = ["RunReport", "report"]

class RunReport(BaseModel):
    started_at: str = ""
    duration_seconds: float = 0.0
    catalogue_pages_crawled: int = 0
    book_urls_discovered: int = 0
    pages_cache_hits: int = 0
    pages_fetched: int = 0
    failed_pages: int = 0
    valid_records: int = 0
    invalid_records: int = 0

class ReportManager:
    _raw_record = {}    
    
    @staticmethod
    def raise_report(apply: Callable[[RunReport], None]) -> None:
        try:
            record = RunReport(**ReportManager._raw_record)
            apply(record)
            ReportManager._raw_record = record.model_dump()
        except ValidationError as e:
            record.invalid_records += 1
    
    @staticmethod
    def freeze_report():
        import json
        
        RUN_REPORT = Path("output/run-report.json")
        RUN_REPORT.parent.mkdir(parents=True, exist_ok=True)
        
        with RUN_REPORT.open("w", encoding="utf-8") as file:
            json.dump(ReportManager._raw_record, file, ensure_ascii=False, indent=2)