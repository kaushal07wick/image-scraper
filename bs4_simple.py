import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():
    urls = [
		    "https://lovable.dev/",
		    "https://www.greptile.com/",
		    "https://cartesia.ai/sonic",
		    "https://exa.ai/",
		    "https://www.raindrop.ai/"
    ]
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = [
            urljoin(url, img["src"])
            for img in soup.find_all("img")
            if img.get("src")
        ]
        print(images)

if __name__ == "__main__":
    main()