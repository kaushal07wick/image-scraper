import os, time, re, requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
BASE = "https://api.firecrawl.dev/v2"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SITES = [
    "https://lovable.dev/",
    "https://www.greptile.com/",
    "https://cartesia.ai/sonic",
    "https://exa.ai/",
    "https://www.raindrop.ai/"
]


def extract_images(markdown: str):
    return list(set(re.findall(r'!\[.*?\]\((https?://[^\)]+)\)', markdown)))


def crawl_site(url, retries=3):
    print(f"\n=== Scraping: {url} ===")

    for attempt in range(retries):
        res = requests.post(
            f"{BASE}/crawl",
            headers=HEADERS,
            json={
                "url": url,
                "limit": 8,  # keep small to avoid throttling
                "scrapeOptions": {
                    "formats": ["markdown"],
                    "onlyMainContent": False,
                    "waitFor": 1500
                }
            }
        )

        if res.status_code == 429:
            wait = 5 + attempt * 3
            print(f"⚠️ Rate limited. Waiting {wait}s...")
            time.sleep(wait)
            continue

        res.raise_for_status()
        job_id = res.json()["id"]
        break
    else:
        print("❌ Failed after retries")
        return []

    while True:
        status = requests.get(f"{BASE}/crawl/{job_id}", headers=HEADERS).json()

        if status["status"] == "completed":
            images = []
            for page in status["data"]:
                images += extract_images(page.get("markdown", ""))

            images = list(set(images))
            print(f"Images: {len(images)}")

            for img in images[:10]:
                print(img)

            return images

        time.sleep(1)


if __name__ == "__main__":
    for site in SITES:
        crawl_site(site)
        time.sleep(4)  # <-- CRITICAL: prevent 429s
