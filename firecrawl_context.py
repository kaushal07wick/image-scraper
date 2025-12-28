"""
Analyze modern startup websites to understand layout patterns,
visual hierarchy, and design systems using Firecrawl.
"""

import os
from dotenv import load_dotenv
from firecrawl import Firecrawl
from pydantic import BaseModel
from typing import List

load_dotenv()
firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

SITES = [
    "https://lovable.dev/",
    "https://www.greptile.com/",
    "https://cartesia.ai/sonic",
    "https://exa.ai/",
    "https://www.raindrop.ai/"
]


class DesignSection(BaseModel):
    title: str
    purpose: str
    visuals: List[str]


class DesignAnalysis(BaseModel):
    sections: List[DesignSection]


for site in SITES:
    print(f"\n==============================")
    print(f"Analyzing: {site}")
    print(f"==============================")

    # Fixed: In v2, formats is an array where json format is an object with type, schema, and prompt
    result = firecrawl.scrape(
        site,
        formats=[
            {
                "type": "json",
                "schema": DesignAnalysis.model_json_schema(),
                "prompt": """
Analyze this website like a product designer.

Identify major layout sections such as:
- Hero
- Product showcase
- Feature breakdown
- Social proof
- Call to action

For each section:
- Give a short title
- Explain the visual purpose
- Include representative image URLs

Ignore icons, logos, UI chrome, and decorative assets.
"""
            },
            "branding"  # branding is a string format
        ],
        timeout=120000
    )

    # Fixed: Access the data correctly from the Document object returned by the Python SDK
    # The SDK returns a Document object with attributes, not a dictionary
    sections = result.json["sections"]
    branding = result.branding

    print(f"\nDesign Sections ({len(sections)}):\n")

    for i, s in enumerate(sections, 1):
        print(f"{i}. {s['title']}")
        print(f"   Purpose: {s['purpose']}")
        for img in s["visuals"][:3]:
            print(f"   - {img}")
        print()

    print("Brand Summary:")
    print(f"  Primary Color: {branding.colors.get('primary', 'N/A')}")
    print(f"  Font: {branding.typography.get('fontFamilies', {}).get('primary', 'N/A')}")
    print(f"  Style: {branding.color_scheme}")