import requests
URLS = ["https://lovable.dev/", "https://www.greptile.com/", "https://cartesia.ai/sonic", "https://exa.ai/", "https://www.raindrop.ai/"]
API = "https://api.firecrawl.dev/v2/scrape"
HEADERS = {"Authorization": "Bearer fc-bd35616d895344df9b4494b78e1e2c8b", "Content-Type": "application/json"}

for url in URLS:
    res = requests.post(API, headers=HEADERS, json={
        "url": url, "onlyMainContent": True, "maxAge": 172800000,
        "formats": ["markdown", "links", "html", "screenshot"]}).json()

    print("URL:", url)
    d = res["data"]; print("Title:", d["metadata"].get("title"), "| Links:", len(d["links"]), "| Markdown:", len(d["markdown"]), "| Screenshot:", "screenshot" in d)