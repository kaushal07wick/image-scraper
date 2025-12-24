<p align="center">
  <img src="https://raw.githubusercontent.com/firecrawl/firecrawl/main/img/firecrawl_logo.png" width="140" alt="Firecrawl logo">
</p>

# Firecrawl Image Scraping

This repository contains all code examples referenced in the Firecrawl image scraping blog. It demonstrates how Firecrawl reliably extracts images, metadata, structured data, and screenshots from modern, JavaScript-heavy websites—without brittle selectors, headless browsers, or manual DOM handling. Each file maps directly to a specific section of the blog and is intentionally focused, minimal, and production-relevant.


## Examples Covered in the Blog

* **[`bs4_simple.py`](bs4_simple.py)**
  A baseline BeautifulSoup scraper for static HTML pages, used to illustrate why traditional parsing fails on modern, JS-driven sites.

* **[`selenium_simple.py`](selenium_simple.py)**
  A minimal Selenium example showing the cost, complexity, and fragility of browser-based scraping.

* **[`firecrawl_simple.py`](firecrawl_simple.py)**
  The simplest Firecrawl `/scrape` example demonstrating clean image extraction via markdown.

* **[`firecrawl_context.py`](firecrawl_context.py)**
  Shows context-aware extraction where images retain page-level meaning without CSS selectors.

* **[`firecrawl_advanced.py`](firecrawl_advanced.py)**
  An end-to-end pipeline combining metadata extraction, image collection, and batch scraping using Firecrawl.

## Future Recommendations

* Use the **`images` format** instead of markdown parsing when you only need raw image URLs.
* Prefer **`batch/scrape`** for galleries, category pages, or multi-URL workflows to reduce latency and cost.
* Combine **screenshots + actions** for highly dynamic or interaction-gated pages.
* Apply filtering (aspect ratio, file size, deduplication) *after* extraction, not during scraping.
* For structured image datasets, pair Firecrawl with the **JSON format** to keep pipelines deterministic.

For deeper details and up-to-date parameters, refer to the official Firecrawl documentation:
[https://docs.firecrawl.dev/introduction](https://docs.firecrawl.dev/introduction)

## License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute these examples for personal or commercial projects, with attribution.

