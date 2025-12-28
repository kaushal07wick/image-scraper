import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# list of startups | you can choose any u want
urls = [
    "https://lovable.dev/",
    "https://www.greptile.com/",
    "https://cartesia.ai/sonic",
    "https://exa.ai/",
    "https://www.raindrop.ai/"
]

for url in urls:
    print(f"\n== {url} ==")
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                print(urljoin(url, src))
    except Exception as e:
        print("Error:", e)
