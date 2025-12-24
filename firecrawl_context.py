import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not set")

BASE_URL = "https://api.firecrawl.dev/v2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

URLS = [
    "https://unsplash.com/s/photos/fire",
]

payload = {
    "urls": URLS,
    "formats": ["images"],
    "onlyMainContent": True,
    "waitFor": 4000,
}

r = requests.post(
    f"{BASE_URL}/batch/scrape",
    json=payload,
    headers=HEADERS,
    timeout=30,
)
r.raise_for_status()

job_id = r.json()["id"]
print(f"Batch job started: {job_id}")

while True:
    status = requests.get(
        f"{BASE_URL}/batch/scrape/{job_id}",
        headers=HEADERS,
        timeout=30,
    )
    status.raise_for_status()
    data = status.json()

    if data.get("status") == "completed":
        results = data.get("data", [])
        break

    if data.get("status") == "failed":
        raise RuntimeError("Batch scrape failed")

    time.sleep(2)

images = []
for page in results:
    images.extend(page.get("images", []))

filtered = [
    url for url in images
    if "images.unsplash.com" in url
]

print(f"\nImages found: {len(images)}")
print(f"Filtered (Unsplash CDN): {len(filtered)}\n")

for img in filtered[:10]:
    print(img)
