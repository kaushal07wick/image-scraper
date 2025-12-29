from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

def rgb_to_hex(rgb: str) -> str:
    if not rgb or not rgb.startswith('rgb'):
        return rgb
    nums = re.findall(r'\d+', rgb)
    if len(nums) >= 3:
        return f'#{int(nums[0]):02x}{int(nums[1]):02x}{int(nums[2]):02x}'
    return rgb

def scrape_with_selenium(url: str) -> dict:
    start_time = time.time()
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
        
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        images = [img.get_attribute('src') for img in driver.find_elements(By.TAG_NAME, 'img')
                  if img.get_attribute('src') and not img.get_attribute('src').startswith('data:')]
        
        colors = set()
        elements = []
        for tag in ['body', 'header', 'main', 'section']:
            elements.extend(driver.find_elements(By.TAG_NAME, tag)[:5])
        elements.extend(driver.find_elements(By.TAG_NAME, 'div')[:50])
        
        for elem in elements:
            try:
                for prop in ['background-color', 'color', 'border-color']:
                    color = elem.value_of_css_property(prop)
                    if color and color not in ['rgba(0, 0, 0, 0)', 'transparent']:
                        hex_color = rgb_to_hex(color)
                        if hex_color.startswith('#'):
                            colors.add(hex_color)
            except:
                pass
        
        fonts = set()
        for tag in ['body', 'h1', 'p']:
            for elem in driver.find_elements(By.TAG_NAME, tag)[:10]:
                try:
                    font = elem.value_of_css_property('font-family').split(',')[0].strip('"\'')
                    if font and font.lower() not in ['serif', 'sans-serif', 'monospace']:
                        fonts.add(font)
                except:
                    pass
        
        sections = len(driver.find_elements(By.TAG_NAME, 'section'))
        
        return {
            'url': url,
            'success': True,
            'time': round(time.time() - start_time, 2),
            'images': len(images),
            'colors': len(colors),
            'fonts': len(fonts),
            'sections': sections,
            'method': 'selenium'
        }
        
    except Exception as e:
        return {
            'url': url,
            'success': False,
            'error': str(e),
            'time': round(time.time() - start_time, 2),
            'method': 'selenium'
        }
    finally:
        if driver:
            driver.quit()

def main():
    sites = [
        "https://lovable.dev/",
        "https://www.greptile.com/",
        "https://cartesia.ai/sonic"
    ]
    
    print("Approach 2: Selenium\n")
    results = []
    
    for i, site in enumerate(sites, 1):
        print(f"[{i}/{len(sites)}] {site}...", end=" ")
        result = scrape_with_selenium(site)
        results.append(result)
        
        if result['success']:
            print(f"✓ {result['time']}s - {result['images']} images, {result['colors']} colors, {result['fonts']} fonts")
        else:
            print(f"✗ Failed")
        
        time.sleep(2)
    
    successful = sum(1 for r in results if r['success'])
    if successful > 0:
        avg_time = sum(r['time'] for r in results if r['success']) / successful
        avg_images = sum(r['images'] for r in results if r['success']) / successful
        avg_colors = sum(r['colors'] for r in results if r['success']) / successful
        
        print(f"\n{'='*60}")
        print(f"Success: {successful}/{len(results)} | Avg Time: {avg_time:.1f}s")
        print(f"Avg Images: {avg_images:.0f} | Avg Colors: {avg_colors:.0f}")
        print(f"\n Works but slow |  Complex setup, manual parsing")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    main()