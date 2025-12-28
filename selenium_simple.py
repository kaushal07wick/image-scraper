import time, os, psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

urls = [
    "https://lovable.dev/",
    "https://www.greptile.com/",
    "https://cartesia.ai/sonic",
    "https://exa.ai/",
    "https://www.raindrop.ai/"
]

def scrape(url):
    start = time.time()
    mem_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    images = set()

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        last = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)
            height = driver.execute_script("return document.body.scrollHeight")
            if height == last:
                break
            last = height

        for img in driver.find_elements(By.TAG_NAME, "img"):
            src = img.get_attribute("src") or img.get_attribute("data-src")
            if src and not src.startswith("data:"):
                images.add(urljoin(url, src))

    finally:
        driver.quit()

    mem_end = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    print(f"\n{url}")
    print(f"Images: {len(images)} | Time: {time.time()-start:.2f}s | Mem: {mem_end-mem_start:.2f}MB")

    return images


for site in urls:
    imgs = scrape(site)
    for i, img in enumerate(list(imgs)[:10], 1):
        print(f"{i}. {img}")
