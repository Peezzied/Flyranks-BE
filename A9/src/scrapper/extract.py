from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .fetch import fetch_cache
from .constants import BookURLs
from datetime import datetime, timezone
from itertools import chain
from pathlib import Path
from pydantic import BaseModel

OUTPUT_PATH = Path("output/book.json")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: str | None = None
    source_page: str
    fetched_at: str

def extract(discovered: BookURLs):
    extracted = []
    unique_urls = set()
    
    for source_url, discovery in discovered.items():
        for source in discovery:
            if source in unique_urls:
                continue
            
            page = fetch_cache(source)
            product = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser").select_one("article.product_page")
            
            record = {
                "title": product.select_one("h1").get_text(strip=True),
                "product_url": source,
                "price_text": product.select_one("p.price_color").get_text(strip=True),
                "availability_text": product.select_one("p.instock.availability").get_text(strip=True),
                "rating_text": product.select_one("p.star-rating").get("class")[1],
                "description": product.select_one("div#product_description + p").get_text(strip=True),
                "source_page": source_url,
                "fetched_at": datetime.fromtimestamp(page.stat().st_birthtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
            record["price_gbp"] = float(record["price_text"][1:])
            
            unique_urls.add(source)
            extracted.append(BookRecord(**record).model_dump())
    
    import json
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump([i for i in extracted], file, ensure_ascii=False, indent=2)
    
    print(f"detail_pages={len(extracted)}")
    
    return extracted
        
        