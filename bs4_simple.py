import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urljoin

def getdata(url): 
    r = requests.get(url) 
    return r.text 

url = "https://www.firecrawl.dev/"
htmldata = getdata(url) 
soup = BeautifulSoup(htmldata, 'html.parser') 

for item in soup.find_all('img'):
    # Get the src attribute
    img_src = item.get('src')
    
    if img_src:
        # Convert relative URLs to absolute URLs
        absolute_url = urljoin(url, img_src)
        print(absolute_url)