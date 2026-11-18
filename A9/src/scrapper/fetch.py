import requests
from pathlib import Path

__all__ = ["fetch"]

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Peezzied/Flyranks-BE/)"


def fetch(url: str, seq: int):
    file = CACHE_DIR / Path(f"catalogue-page-{seq}.html")
    
    if file.exists():
        print("CACHE HIT")
        print(f"{file.stat().st_size:,} bytes")
        return
    
    req = requests.get(url.strip(), timeout=10, headers={
        "User-Agent": USER_AGENT
    })
    
    if req.status_code != 200:
        return
    
    print("FETCH")
    print(f"{len(req.content):,} bytes")
    
    file.write_text(req.text, encoding="utf-8")