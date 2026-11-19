import requests
import time
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse, urlsplit
from .constants import CACHE_DIR

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
        return file
    
    req = requests.get(url.strip(), timeout=10, headers={
        "User-Agent": USER_AGENT
    })
    req.encoding = "utf-8"
    
    if req.status_code != 200:
        return None
    
    print("FETCH")
    print(f"{len(req.content):,} bytes")
    
    file.write_text(req.text, encoding="utf-8")
    time.sleep(0.5)
    return file