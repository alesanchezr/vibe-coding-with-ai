#!/usr/bin/env python3

import json
import os

def create_seo_rule():
    # Language mapping dictionary
    language_map = {
        "es": "español",
        "en": "english",
        "us": "english",
        "zh": "chinese",
        "it": "italian",
        "cn": "chinese",
        # Add more language mappings as needed
    }
    
    # Read the clusters data
    try:
        with open("scripts/clusters.json", "r") as f:
            clusters = json.load(f)
    except FileNotFoundError:
        print("Error: clusters.json file not found in scripts directory")
        return
    except json.JSONDecodeError:
        print("Error: clusters.json is not valid JSON")
        return

    # Create the rule content
    rule_content = """# SEO Cluster Linking Rule

This rule helps ensure that new articles link to appropriate landing pages within their topic clusters.

## Landing Pages to Link To

When writing a new article, consider linking to these relevant landing pages:

"""

    # Add each cluster's landing page information with language
    for cluster in clusters:
        # Skip clusters with empty landing page URLs
        if "title" in cluster and "landing_page_url" in cluster and cluster["landing_page_url"]:
            # Get language from cluster or use "Unknown" if not available
            lang_code = cluster.get("lang", "").lower()
            # Map language code to full name or use the code if not in mapping
            language = language_map.get(lang_code, lang_code) if lang_code else "Unknown"
            rule_content += f"- **{cluster['title']}** [{language}]: [{cluster['landing_page_url']}]({cluster['landing_page_url']})\n"
    
    rule_content += """
## Guidelines

1. Each article should link to its cluster's landing page at least once
2. Use descriptive anchor text that includes relevant keywords
3. Place links naturally within the content where they provide value to readers
4. Avoid excessive linking that could appear spammy

## Implementation

When writing content related to any of these topics, include contextually relevant links to the appropriate landing pages.
"""

    # Create the rules directory if it doesn't exist
    os.makedirs(".cursor/rules", exist_ok=True)

    # Write the rule file
    try:
        with open(".cursor/rules/seo.mdc", "w") as f:
            f.write(rule_content)
        print("SEO rule created successfully at .cursor/rules/seo.mdc")
    except Exception as e:
        print(f"Error writing rule file: {e}")

if __name__ == "__main__":
    create_seo_rule()
