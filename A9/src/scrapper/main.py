from .discover import discover
from .extract import extract
from datetime import datetime, timezone
from .reports import ReportManager
from argparse import Namespace
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pages", type=int, default=3)
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    
    start_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ReportManager.raise_report(lambda x: setattr(x, "started_at", start_iso))
    start_perf = time.perf_counter()
    
    # Do run job
    extract(discover(3 if not args.pages else args.pages))
    
    duration_seconds = round(time.perf_counter() - start_perf, 2)
    ReportManager.raise_report(lambda x: setattr(x, "duration_seconds", duration_seconds))
    
    ReportManager.freeze_report()