# Scrapper

Scrapper shows polite web scraping in Python. It turns three catalogue pages of HTML into 60 clean, checked JSON records.

## Classification

### Target classification

`https://books.toscrape.com/` is a fictional bookstore sandbox. The site exists for scraping practice, so it is a safe target.

Stage 0 classified the target as:

* **Public.** No login and no paywall.
* **Static HTML.** The server sends the book data in the HTML response.
* **Missing `robots.txt`.** `https://books.toscrape.com/robots.txt` returns 404.
* **Small and stable.** The catalogue uses simple links and product pages.
* **Three catalogue pages.** Stage 0 named the Philosophy, Classics, and Science Fiction catalogue pages:
  * https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html
  * https://books.toscrape.com/catalogue/category/books/classics_6/index.html
  * https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html

The delivered crawler follows the `next` links from the main catalogue. Thus the run covers catalogue pages 1 to 3, which is 60 book detail pages:

* https://books.toscrape.com/catalogue/page-1.html
* https://books.toscrape.com/catalogue/page-2.html
* https://books.toscrape.com/catalogue/page-3.html

Both scopes are public catalogue pages on the same sandbox. The run report below reflects the delivered crawl.

## Usage

**Stack:** Python 3.14, `uv`, `requests`, `beautifulsoup4`, and `pydantic`.

Install from the `A9` directory:

```bash
uv sync
```

### Run

```bash
cd A9 && uv sync && uv run scrapper
```

The command accepts `-p N` to set the number of catalogue pages. The default is 3.

```bash
uv run scrapper -p 1
```

The run writes two files:

* `output/book.json` — the valid records.
* `output/run-report.json` — the counters for the run.

## Record schema

Each book is a Pydantic model. A record that fails validation is not written to `book.json`, and `invalid_records` increases.

| Field | Type | Description |
| :--- | :--- | :--- |
| `title` | `str` | Book title from the product page heading. |
| `product_url` | `str` | Absolute URL of the book detail page. |
| `price_text` | `str` | Price as shown, for example `£51.77`. |
| `price_gbp` | `float` | Numeric price in GBP, for example `51.77`. |
| `availability_text` | `str` | Stock text, for example `In stock (22 available)`. |
| `rating_text` | `str` | Star rating as a word, for example `Three`. |
| `description` | `str` or `null` | Product description text. |
| `source_page` | `str` | Catalogue page that linked to the book. |
| `fetched_at` | `str` | UTC timestamp in ISO 8601 format. |

## Politeness rules

| Rule | Implementation |
| :--- | :--- |
| **User-Agent** | `FlyRankInternship-A9/1.0 (+https://github.com/Peezzied/Flyranks-BE/)`. The request identifies the project and gives a contact URL. |
| **Delay** | `time.sleep(0.5)` after each network fetch. Cache hits do not sleep. |
| **Timeout** | 10 seconds for each request. A slow server does not hold the run open. |
| **Retries** | 3 retries with a backoff factor of 1. The retry set is 500, 502, 503, and 504. The client obeys the `Retry-After` header. |
| **Cache** | Each response goes to `cache/`. A later run reads the local file first and sends no request for a cache hit. |
| **Scope** | Three catalogue pages and their 60 book detail pages. The crawler follows no link outside this scope. |

## Run report

This is a real run on 2026-11-24. The cache was warm, so the run made zero network requests and served 63 pages from disk.

```json
{
  "started_at": "2026-11-24T07:59:49Z",
  "duration_seconds": 0.76,
  "catalogue_pages_crawled": 3,
  "book_urls_discovered": 60,
  "pages_cache_hits": 63,
  "pages_fetched": 0,
  "failed_pages": 0,
  "valid_records": 60,
  "invalid_records": 0
}
```

## Why no browser

The data is already in the HTML the server sends, so a browser would only add cost.

## One honest limitation

The cache never expires. The code checks only whether a cache file exists, so a later run reuses old HTML and reports `pages_fetched: 0`. The `fetched_at` value also comes from the cache file time, not from the current run. Delete `cache/` before a run when you need fresh data.

## Ethics

Use an official API when one exists. A supported endpoint is cheaper and more reliable than a parser. Never bypass a login, a paywall, or a block. Collect only the data you need for the task, and stop when the site says no.

---
<p align="center">
<i>Disclaimer: I will not reuse this code on another site without checking its rules and terms first.</i>
</br> 
<b>Note:</b> This is a Flyranks assignment for Backend AI Engineering. 
</p>