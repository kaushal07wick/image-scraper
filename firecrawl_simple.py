import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not set")

url = "https://api.firecrawl.dev/v2/scrape"

payload = {
    "url": "https://firecrawl.dev",
    "onlyMainContent": True,
    "maxAge": 172800000,
    "parsers": [],
    "formats": ["markdown"],
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

response = requests.post(url, json=payload, headers=headers, timeout=30)
response.raise_for_status()

data = response.json()

if not data.get("success"):
    raise RuntimeError(data)

markdown_content = data["data"].get("markdown", "")

heading_match = re.search(r"^#\s+(.+)$", markdown_content, re.MULTILINE)
if heading_match:
    print(f"Heading: {heading_match.group(1)}\n")

image_pattern = r"!\[.*?\]\((https?://[^\)]+)\)"
image_urls = re.findall(image_pattern, markdown_content)

unique_images = list(dict.fromkeys(image_urls))

print(f"Found {len(unique_images)} unique images:\n")
for idx, img_url in enumerate(unique_images, 1):
    print(f"{idx}. {img_url}")
