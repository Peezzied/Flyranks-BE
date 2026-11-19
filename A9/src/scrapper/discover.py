from .fetch import fetch_cache
from bs4 import BeautifulSoup
from urllib.parse import urljoin 

__all__ = ["discover"]

RELATIVE_TO = "https://books.toscrape.com/catalogue/"

def _go_next(html: str):
    parse = BeautifulSoup(html, "html.parser")
    next_link = parse.find("a", string="next")
    assert next_link is not None
    return parse, urljoin(RELATIVE_TO, str(next_link.get("href")))

def discover(catalogue_pages=3) -> list[str]:
    first_catalogue_cache = fetch_cache("https://books.toscrape.com/catalogue/page-1.html")
    if not first_catalogue_cache:
        return []
    
    page = first_catalogue_cache.read_text(encoding="utf-8")
    discovered_books: list[str] = []
    
    for i in range(0, catalogue_pages):
        parsed_page, next_url = _go_next(page)
        books_parsed_url = [urljoin(RELATIVE_TO, str(i.get("href"))) for i in parsed_page.find_all("a", title=True)]
    
        discovered_books.extend(books_parsed_url)
        
        if i == catalogue_pages-1:
            break
        
        page = fetch_cache(next_url).read_text(encoding="utf-8")
    
    print(f"catalogue_pages={catalogue_pages}, discovered={len(discovered_books)}, unique_urls={len(set(discovered_books))}")
    
    return discovered_books