import os, requests
from dotenv import load_dotenv; load_dotenv()

urls = ["https://lovable.dev/"]

for url in urls:
    r = requests.post(
        "https://api.firecrawl.dev/v2/scrape",
        headers={"Authorization": f"Bearer {os.getenv('FIRECRAWL_API_KEY')}"},
        json={"url": url, "formats": ["images"]},
    )
    print(f"\n{url}")
    print(r.json()["data"]["images"])