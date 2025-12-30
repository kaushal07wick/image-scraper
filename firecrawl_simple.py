import requests

URLS = [
    "https://lovable.dev/",
    "https://www.greptile.com/",
    "https://cartesia.ai/sonic",
    "https://exa.ai/",
    "https://www.raindrop.ai/",
]

API_URL = "https://api.firecrawl.dev/v2/scrape"

HEADERS = {
    "Authorization": "Bearer fc-bd35616d895344df9b4494b78e1e2c8b",
    "Content-Type": "application/json"
}

for url in URLS:
    payload = {
        "url": url,
        "onlyMainContent": True,
        "maxAge": 172800000,
        "formats": ["markdown", "links", "html", "screenshot"]
    }

    res = requests.post(API_URL, json=payload, headers=HEADERS)
    data = res.json()

    print("\n" + "=" * 60)
    print(f"URL: {url}")

    if not data.get("success"):
        print("❌ Error:", data)
        continue

    d = data.get("data", {})
    print("Title:", d.get("metadata", {}).get("title"))
    print("Links:", len(d.get("links", [])))
    print("Markdown length:", len(d.get("markdown", "")))
    print("Has screenshot:", "screenshot" in d)
