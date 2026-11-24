from pathlib import Path

CACHE_DIR = Path("cache")
RELATIVE_URL = "https://books.toscrape.com/catalogue/"

type BookURLs = dict[str, list[str]]