import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse, urlsplit
from .constants import CACHE_DIR
from .reports import ReportManager

__all__ = ["fetch_cache"]

CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Peezzied/Flyranks-BE/)"

def fetch_cache(url: str) -> Path | None:
    file = CACHE_DIR / Path("-".join(
        str(PurePosixPath(urlparse(url).path).with_suffix("").relative_to("/")).split("/")
    )).with_suffix(".html")
    
    if file.exists():
        print("CACHE HIT")
        print(f"{file.stat().st_size:,} bytes")
        ReportManager.raise_report(lambda x: setattr(x, "pages_cache_hits", x.pages_cache_hits + 1))
        
        return file
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        respect_retry_after_header=True,
    )
    
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    
    req = session.get(url.strip(), timeout=10, headers={
        "User-Agent": USER_AGENT
    })
    req.encoding = "utf-8"
    
    if req.status_code != 200:
        ReportManager.raise_report(lambda x: setattr(x, "failed_pages", x.failed_pages + 1))
        return None
    
    print("FETCH")
    print(f"{len(req.content):,} bytes")
    ReportManager.raise_report(lambda x: setattr(x, "pages_fetched", x.pages_fetched + 1))
    
    file.write_text(req.text, encoding="utf-8")
    time.sleep(0.5)
    return file