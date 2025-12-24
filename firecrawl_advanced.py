import requests
import re
import time
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AdvancedFirecrawlImageScraper:
    def __init__(self, api_key: str = None):
        # Try to get API key from parameter, environment variable, or raise error
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "API key not found. Please set FIRECRAWL_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.base_url = "https://api.firecrawl.dev/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def scrape_single_page_with_metadata(self, url: str) -> Dict:
        """
        Scrape a single page and extract images with full metadata
        """
        print(f"\n{'='*60}")
        print(f"Scraping: {url}")
        print(f"{'='*60}\n")
        
        payload = {
            "url": url,
            "formats": ["markdown", "html"],
            "onlyMainContent": False,  # Get all content including headers/footers
            "includeTags": ["img", "picture", "figure"],  # Focus on image-related tags
            "waitFor": 2000  # Wait for lazy-loaded images
        }
        
        response = requests.post(
            f"{self.base_url}/scrape",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['data']
                
                # Extract metadata
                metadata = result.get('metadata', {})
                print(f"Page Title: {metadata.get('title')}")
                print(f"Description: {metadata.get('description')}")
                print(f"Language: {metadata.get('language')}")
                print(f"OG Image: {metadata.get('ogImage')}")
                print(f"Status Code: {metadata.get('statusCode')}")
                print(f"Robots: {metadata.get('robots')}\n")
                
                # Extract images from markdown
                markdown_content = result.get('markdown', '')
                image_pattern = r'!\[([^\]]*)\]\((https?://[^\)]+)\)'
                images = re.findall(image_pattern, markdown_content)
                
                unique_images = []
                seen = set()
                for alt_text, img_url in images:
                    if img_url not in seen:
                        seen.add(img_url)
                        unique_images.append({
                            'url': img_url,
                            'alt_text': alt_text,
                            'page_url': metadata.get('sourceURL'),
                            'page_title': metadata.get('title')
                        })
                
                print(f"Found {len(unique_images)} unique images\n")
                return {
                    'metadata': metadata,
                    'images': unique_images,
                    'total_images': len(unique_images)
                }
        
        return {'error': 'Failed to scrape', 'status_code': response.status_code}
    
    def batch_scrape_with_rate_limiting(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        Scrape multiple URLs with built-in rate limiting
        Uses Firecrawl's batch endpoint for efficiency
        """
        print(f"\n{'='*60}")
        print(f"Batch Scraping {len(urls)} URLs")
        print(f"{'='*60}\n")
        
        payload = {
            "urls": urls,
            "formats": ["markdown"],
            "onlyMainContent": True
        }
        
        # Start batch scrape job
        response = requests.post(
            f"{self.base_url}/batch/scrape",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 200:
            job_data = response.json()
            job_id = job_data['id']
            print(f"Batch job started: {job_id}")
            print("Waiting for completion...\n")
            
            # Poll for completion
            while True:
                status_response = requests.get(
                    f"{self.base_url}/batch/scrape/{job_id}",
                    headers=self.headers
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data.get('status')
                    completed = status_data.get('completed', 0)
                    total = status_data.get('total', len(urls))
                    
                    print(f"Status: {status} | Progress: {completed}/{total}")
                    
                    if status == 'completed':
                        results = []
                        for page in status_data.get('data', []):
                            markdown = page.get('markdown', '')
                            metadata = page.get('metadata', {})
                            
                            # Extract images
                            image_pattern = r'!\[([^\]]*)\]\((https?://[^\)]+)\)'
                            images = re.findall(image_pattern, markdown)
                            
                            unique_images = list(set([img[1] for img in images]))
                            
                            results.append({
                                'url': metadata.get('sourceURL'),
                                'title': metadata.get('title'),
                                'images': unique_images,
                                'image_count': len(unique_images)
                            })
                        
                        print(f"\nBatch scraping completed!")
                        print(f"Credits used: {status_data.get('creditsUsed')}\n")
                        return results
                    
                    elif status == 'failed':
                        print("Batch job failed")
                        return []
                
                time.sleep(delay)
        
        return []
    
    def crawl_website_for_images(self, start_url: str, max_pages: int = 10) -> Dict:
        """
        Crawl an entire website and extract all images
        Respects robots.txt by default
        """
        print(f"\n{'='*60}")
        print(f"Crawling Website: {start_url}")
        print(f"Max Pages: {max_pages}")
        print(f"{'='*60}\n")
        
        payload = {
            "url": start_url,
            "limit": max_pages,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True
            },
            "maxDepth": 2  # How deep to follow links
        }
        
        # Start crawl job
        response = requests.post(
            f"{self.base_url}/crawl",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 200:
            job_data = response.json()
            job_id = job_data['id']
            print(f"Crawl job started: {job_id}")
            print("Crawling in progress...\n")
            
            # Poll for completion
            while True:
                status_response = requests.get(
                    f"{self.base_url}/crawl/{job_id}",
                    headers=self.headers
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data.get('status')
                    total = status_data.get('total', 0)
                    completed = status_data.get('completed', 0)
                    
                    print(f"Status: {status} | Pages crawled: {completed}/{total}")
                    
                    if status == 'completed':
                        all_images = []
                        page_summaries = []
                        
                        for page in status_data.get('data', []):
                            markdown = page.get('markdown', '')
                            metadata = page.get('metadata', {})
                            
                            # Extract images
                            image_pattern = r'!\[([^\]]*)\]\((https?://[^\)]+)\)'
                            images = re.findall(image_pattern, markdown)
                            
                            unique_images = list(set([img[1] for img in images]))
                            all_images.extend(unique_images)
                            
                            page_summaries.append({
                                'url': metadata.get('sourceURL'),
                                'title': metadata.get('title'),
                                'image_count': len(unique_images)
                            })
                        
                        # Deduplicate all images
                        unique_all_images = list(set(all_images))
                        
                        print(f"\nCrawl completed!")
                        print(f"Total pages crawled: {total}")
                        print(f"Total unique images found: {len(unique_all_images)}")
                        print(f"Credits used: {status_data.get('creditsUsed')}\n")
                        
                        return {
                            'total_pages': total,
                            'total_images': len(unique_all_images),
                            'images': unique_all_images,
                            'page_summaries': page_summaries,
                            'credits_used': status_data.get('creditsUsed')
                        }
                    
                    elif status == 'failed':
                        print("Crawl job failed")
                        return {}
                
                time.sleep(2)
        
        return {}
    
    def filter_images_by_criteria(self, images: List[str], 
                                  min_size: bool = True,
                                  exclude_patterns: List[str] = None) -> List[str]:
        """
        Filter images based on criteria
        """
        if exclude_patterns is None:
            exclude_patterns = ['icon', 'logo', 'avatar', 'thumbnail']
        
        filtered = []
        for img_url in images:
            # Skip tracking pixels and tiny images
            if any(pattern in img_url.lower() for pattern in exclude_patterns):
                continue
            
            # Skip data URIs
            if img_url.startswith('data:'):
                continue
            
            # Check if URL contains size indicators (optional)
            if min_size and ('w=48' in img_url or 'w=64' in img_url):
                continue
            
            filtered.append(img_url)
        
        return filtered
    
    def generate_report(self, results: Dict, output_file: str = 'image_scrape_report.json'):
        """
        Generate a JSON report of all scraped images
        """
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nReport saved to: {output_file}")


# Usage Example
def main():
    # API key is loaded from environment variable
    try:
        scraper = AdvancedFirecrawlImageScraper()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nTo fix this, create a .env file with:")
        print("FIRECRAWL_API_KEY=fc-your-api-key-here")
        return
    
    print("="*60)
    print("ADVANCED FIRECRAWL IMAGE SCRAPING DEMO")
    print("="*60)
    
    # Example 1: Single page with metadata
    print("\n### EXAMPLE 1: Single Page Scraping with Metadata ###")
    single_result = scraper.scrape_single_page_with_metadata("https://firecrawl.dev")
    print(f"Extracted {single_result.get('total_images', 0)} images from single page")
    
    # Example 2: Batch scraping multiple URLs
    print("\n### EXAMPLE 2: Batch Scraping Multiple URLs ###")
    urls_to_scrape = [
        "https://firecrawl.dev",
        "https://unsplash.com/",
        "https://www.pexels.com/"
    ]
    batch_results = scraper.batch_scrape_with_rate_limiting(urls_to_scrape, delay=2.0)
    
    for result in batch_results:
        print(f"\n{result['url']}")
        print(f"  Title: {result['title']}")
        print(f"  Images: {result['image_count']}")
    
    # Example 3: Crawl entire website
    print("\n### EXAMPLE 3: Crawling Entire Website ###")
    crawl_results = scraper.crawl_website_for_images("https://firecrawl.dev", max_pages=5)
    
    # Example 4: Filter images
    print("\n### EXAMPLE 4: Filtering Images ###")
    all_images = crawl_results.get('images', [])
    filtered_images = scraper.filter_images_by_criteria(
        all_images,
        exclude_patterns=['icon', 'avatar', 'logo']
    )
    print(f"Before filtering: {len(all_images)} images")
    print(f"After filtering: {len(filtered_images)} images")
    
    # Generate final report
    final_report = {
        'single_page': single_result,
        'batch_scrape': batch_results,
        'crawl': crawl_results,
        'filtered_images': filtered_images
    }
    
    scraper.generate_report(final_report)
    
    print("\n" + "="*60)
    print("SCRAPING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()