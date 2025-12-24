import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not set")

payload = {
    "url": "https://unsplash.com/s/photos/fire",
    "formats": ["images"],
    "onlyMainContent": True,
    "waitFor": 4000
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

r = requests.post(
    "https://api.firecrawl.dev/v2/scrape",
    json=payload,
    headers=headers,
    timeout=30,
)
r.raise_for_status()

images = r.json()["data"].get("images", [])

print(f"Found {len(images)} images")
for img in images[:10]:
    print(img)
