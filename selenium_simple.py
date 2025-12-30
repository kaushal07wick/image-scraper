from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_images(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # allow JS + lazy loading
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    images = [
        img.get_attribute("src")
        for img in driver.find_elements(By.CSS_SELECTOR, "img[src]")
        if not img.get_attribute("src").startswith("data:")
    ]

    driver.quit()
    return images


def main():
    urls = [
        "https://lovable.dev/",
        "https://www.greptile.com/",
        "https://cartesia.ai/sonic",
        "https://exa.ai/",
        "https://www.raindrop.ai/",
    ]

    for url in urls:
        print(url)
        for img in scrape_images(url)[:2]:
            print(img)
        print("...\n")


if __name__ == "__main__":
    main()