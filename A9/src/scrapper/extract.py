from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .fetch import fetch_cache
from .constants import BookURLs
from datetime import datetime, timezone
from itertools import chain

def extract(discovered: BookURLs):
    extracted = []
    
    for source_url, discovery in discovered.items():
        for source in discovery:
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
            
            extracted.append(record)
    print(f"detail_pages={len(extracted)}")
    
    return extracted
        
        