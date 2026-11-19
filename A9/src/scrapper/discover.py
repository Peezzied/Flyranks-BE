from .fetch import fetch_cache
from bs4 import BeautifulSoup
from .constants import BookURLs, RELATIVE_URL
from urllib.parse import urljoin 

__all__ = ["discover"]

def _go_next(html: str):
    parse = BeautifulSoup(html, "html.parser")
    next_link = parse.find("a", string="next")
    assert next_link is not None
    return parse, urljoin(RELATIVE_URL, str(next_link.get("href")))

def discover(catalogue_pages=3) -> BookURLs:
    first_catalogue_url = "https://books.toscrape.com/catalogue/page-1.html"
    first_catalogue_cache = fetch_cache(first_catalogue_url)
    if not first_catalogue_cache:
        return {}
    
    page = first_catalogue_url, first_catalogue_cache.read_text(encoding="utf-8")
    discovered_books = {}
    
    for i in range(0, catalogue_pages):
        url, html = page
        parsed_page, next_url = _go_next(html)
        books_parsed_url = [urljoin(RELATIVE_URL, str(i.get("href"))) for i in parsed_page.find_all("a", title=True)]
    
        discovered_books[url] = books_parsed_url
        
        if i == catalogue_pages-1:
            break
        
        page = next_url, fetch_cache(next_url).read_text(encoding="utf-8")
    
    print(f"catalogue_pages={catalogue_pages}, discovered={len(discovered_books)}, unique_urls={len(set(discovered_books))}")
    
    return discovered_books