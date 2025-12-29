import os
from dotenv import load_dotenv
from firecrawl import Firecrawl
from pydantic import BaseModel
from typing import List
import time
import json
from collections import Counter

load_dotenv()

class DesignSection(BaseModel):
    title: str
    purpose: str
    visual_hierarchy: str
    key_elements: List[str]
    image_urls: List[str]

class DesignAnalysis(BaseModel):
    sections: List[DesignSection]
    primary_message: str
    target_audience: str
    design_philosophy: str

def analyze_site(url: str, firecrawl: Firecrawl) -> dict:
    start_time = time.time()
    
    try:
        result = firecrawl.scrape(
            url,
            formats=[
                {
                    "type": "json",
                    "schema": DesignAnalysis.model_json_schema(),
                    "prompt": """Analyze this website as a senior product designer.
                    
                    Identify sections: Hero, Product Showcase, Features, Social Proof, Pricing, CTA, Footer.
                    For each: title, purpose, visual hierarchy, key elements, important image URLs.
                    
                    Provide: primary message, target audience, design philosophy."""
                },
                "branding"
            ],
            timeout=120000
        )
        
        analysis = result.json
        branding = result.branding
        
        return {
            'url': url,
            'success': True,
            'time': round(time.time() - start_time, 2),
            'sections': analysis.get('sections', []),
            'message': analysis.get('primary_message', ''),
            'audience': analysis.get('target_audience', ''),
            'philosophy': analysis.get('design_philosophy', ''),
            'color_scheme': branding.color_scheme,
            'colors': branding.colors,
            'fonts': branding.typography.get('fontFamilies', {}),
            'typography': branding.typography,
            'spacing': getattr(branding, 'spacing', {}),
        }
        
    except Exception as e:
        return {'url': url, 'success': False, 'error': str(e)}

def generate_markdown(results: List[dict]) -> str:
    successful = [r for r in results if r.get('success')]
    
    md = "# Startup Design Analysis Report\n\n"
    md += f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += f"**Sites Analyzed:** {len(successful)}/{len(results)}\n\n"
    
    md += "---\n\n"
    
    for i, result in enumerate(successful, 1):
        md += f"## {i}. {result['url']}\n\n"
        
        md += "### Brand Identity\n\n"
        md += f"- **Color Scheme:** {result['color_scheme']}\n"
        md += f"- **Primary Color:** {result['colors'].get('primary', 'N/A')}\n"
        md += f"- **Primary Font:** {result['fonts'].get('primary', 'N/A')}\n\n"
        
        md += "### Strategic Analysis\n\n"
        md += f"**Message:** {result['message']}\n\n"
        md += f"**Audience:** {result['audience']}\n\n"
        md += f"**Philosophy:** {result['philosophy']}\n\n"
        
        md += "### Page Sections\n\n"
        for j, section in enumerate(result['sections'], 1):
            md += f"#### {j}. {section['title']}\n\n"
            md += f"**Purpose:** {section['purpose']}\n\n"
            md += f"**Hierarchy:** {section['visual_hierarchy']}\n\n"
            md += f"**Elements:** {', '.join(section['key_elements'])}\n\n"
            if section['image_urls']:
                md += f"**Images:** {len(section['image_urls'])} found\n\n"
        
        md += "---\n\n"
    
    if successful:
        md += "## Aggregate Trends\n\n"
        
        color_schemes = Counter([r['color_scheme'] for r in successful])
        md += "### Color Schemes\n\n"
        for scheme, count in color_schemes.items():
            pct = (count / len(successful)) * 100
            md += f"- **{scheme}:** {count} ({pct:.0f}%)\n"
        md += "\n"
        
        fonts = []
        for r in successful:
            if r['fonts'].get('primary'):
                fonts.append(r['fonts']['primary'])
        font_count = Counter(fonts)
        
        md += "### Popular Fonts\n\n"
        for font, count in font_count.most_common(5):
            md += f"- **{font}:** {count} sites\n"
        md += "\n"
        
        all_sections = []
        for r in successful:
            all_sections.extend([s['title'] for s in r['sections']])
        section_count = Counter(all_sections)
        
        md += "### Common Sections\n\n"
        for section, count in section_count.most_common(10):
            md += f"- **{section}:** {count} occurrences\n"
        md += "\n"
        
        md += "### Design Philosophies\n\n"
        for i, r in enumerate(successful, 1):
            md += f"{i}. {r['philosophy']}\n"
        md += "\n"
    
    return md

def main():
    sites = [
        "https://lovable.dev/",
        "https://www.greptile.com/",
        "https://cartesia.ai/sonic",
        "https://exa.ai/",
        "https://www.raindrop.ai/"
    ]
    
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    results = []
    
    print("Analyzing startup design patterns...\n")
    
    for i, site in enumerate(sites, 1):
        print(f"[{i}/{len(sites)}] {site}...", end=" ")
        result = analyze_site(site, firecrawl)
        results.append(result)
        
        if result['success']:
            print(f"✓ {result['time']}s")
        else:
            print(f"✗ {result.get('error', 'Failed')}")
        
        time.sleep(1)
    
    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    markdown = generate_markdown(results)
    with open('analysis_report.md', 'w') as f:
        f.write(markdown)
    
    print(f"\n Complete!")
    print(f"   • JSON: analysis_results.json")
    print(f"   • Report: analysis_report.md")

if __name__ == "__main__":
    main()