from .fetch import fetch

def main() -> None:
    fetch(url="https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html", seq=1)