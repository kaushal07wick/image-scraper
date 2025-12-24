from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time
import psutil
import os
def scrape_images_selenium(url):
    # Record start time and initial memory
    start_time = time.time()
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    print(f"Starting Selenium scraper...")
    print(f"Initial memory usage: {initial_memory:.2f} MB\n")
    
    # Set up Chrome driver with headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Wait for images to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
        
        # Scroll to trigger lazy loading
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Find all images after scrolling
        images = driver.find_elements(By.TAG_NAME, "img")
        
        image_urls = []
        for img in images:
            img_url = img.get_attribute('src') or img.get_attribute('data-src')
            
            if img_url and not img_url.startswith('data:'):
                absolute_url = urljoin(url, img_url)
                image_urls.append(absolute_url)
        
        # Remove duplicates
        unique_images = list(dict.fromkeys(image_urls))
        
        # Performance summary
        end_time = time.time()
        final_memory = process.memory_info().rss / 1024 / 1024
        
        print(f"Total execution time: {end_time - start_time:.2f} seconds")
        print(f"Peak memory usage: {final_memory:.2f} MB")
        print(f"Memory overhead: {final_memory - initial_memory:.2f} MB\n")
        
        return unique_images
    
    finally:
        driver.quit()
# Usage
url = "https://www.firecrawl.dev/"
images = scrape_images_selenium(url)
print(f"Found {len(images)} unique images\n")
for idx, img_url in enumerate(images[:10], 1):
    print(f"{idx}. {img_url}")