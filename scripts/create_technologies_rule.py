#!/usr/bin/env python3

import json
import os

def create_technologies_rule():
    # Language mapping dictionary
    language_map = {
        "es": "Spanish",
        "en": "English",
        "us": "English",
        "zh": "Chinese",
        "it": "Italian",
        "cn": "Chinese",
        "fr": "French",
        "pt": "Portuguese",
        "de": "German",
        # Add more language mappings as needed
    }
    
    # Read the technologies data
    try:
        with open("scripts/technologies.json", "r") as f:
            technologies = json.load(f)
    except FileNotFoundError:
        print("Error: technologies.json file not found in scripts directory")
        return
    except json.JSONDecodeError:
        print("Error: technologies.json is not valid JSON")
        return

    # Process technologies to remove duplicates and clean data
    tech_dict = {}  # Use dictionary with slug as key to remove duplicates
    
    for tech in technologies:
        slug = tech.get("slug", "")
        if not slug:
            continue  # Skip entries without a slug
            
        # Skip deprecated technologies
        if tech.get("is_deprecated", False):
            continue
            
        # Only keep the first entry for each slug (or the one with a description if available)
        if slug not in tech_dict or (not tech_dict[slug].get("description") and tech.get("description")):
            # Clean up description - limit length and remove newlines
            if "description" in tech and tech["description"]:
                # Truncate description if it's too long
                description = tech["description"]
                if len(description) > 100:
                    description = description[:97] + "..."
                # Replace newlines with spaces
                description = description.replace("\n", " ")
                tech["description"] = description
                
            tech_dict[slug] = tech
    
    # Group technologies by language (if applicable)
    tech_by_lang = {}
    for tech in tech_dict.values():
        lang_code = tech.get("lang")
        
        # Map language code to full name
        if lang_code in language_map:
            lang = language_map[lang_code]
        else:
            lang = lang_code
            
        if lang not in tech_by_lang:
            tech_by_lang[lang] = []
        tech_by_lang[lang].append(tech)
    
    # Create the rule content
    rule_content = """# Approved Technologies Rule

This rule defines the only technologies that should be used in frontmatter or learn.json files.

## Approved Technologies

Below is a comprehensive list of all approved technologies, organized by language (where applicable):

"""

    # First add technologies with no specified language
    if None in tech_by_lang:
        general_techs = tech_by_lang[None]
        rule_content += f"### Multilang Technologies ({len(general_techs)})\n\n"
        for tech in sorted(general_techs, key=lambda x: x["title"].lower()):
            rule_content += f"- {tech['slug']}\n"
        rule_content += "\n"
    
    # Then add technologies grouped by language
    # Sort language keys, treating None as the lowest value
    sorted_langs = sorted([k for k in tech_by_lang.keys() if k is not None])
    
    for lang in sorted_langs:
        lang_techs = tech_by_lang[lang]
        rule_content += f"### {lang} Technologies ({len(lang_techs)})\n\n"
        for tech in sorted(lang_techs, key=lambda x: x["title"].lower()):
            rule_content += f"- {tech['slug']}\n"
        rule_content += "\n"
    
    # Add summary section with the total count
    rule_content += f"## Summary\n\n"
    rule_content += f"Total number of approved technologies: {len(tech_dict)}\n\n"
    
    # Add counts by language
    rule_content += "### Counts by Language\n\n"
    if None in tech_by_lang:
        rule_content += f"- General: {len(tech_by_lang[None])}\n"
    for lang in sorted_langs:
        rule_content += f"- {lang}: {len(tech_by_lang[lang])}\n"
    rule_content += "\n"
    
    # Add guidelines and implementation sections (not using f-string)
    rule_content += """## Guidelines

1. Only use technologies from this approved list in frontmatter or learn.json files
2. Use the exact slug as shown in parentheses (e.g., `html`, `javascript`)
3. Technologies not on this list require approval before use
4. If a technology is missing that you need, please request it to be added to the official registry

## Implementation

When specifying technologies in frontmatter or learn.json files, ensure they match exactly with the approved slugs listed above.

Example frontmatter:
```yaml
technologies: ["javascript", "react", "html", "css"]
```

Example learn.json:
```json
{
  "technologies": ["python", "flask", "sqlalchemy"]
}
```
"""

    # Create the rules directory if it doesn't exist
    os.makedirs(".cursor/rules", exist_ok=True)

    # Write the rule file
    try:
        with open(".cursor/rules/all-technologies.mdc", "w") as f:
            f.write(rule_content)
        print(f"Technologies rule created successfully at .cursor/rules/all-technologies.mdc")
        print(f"Processed {len(tech_dict)} unique technologies (excluding deprecated)")
    except Exception as e:
        print(f"Error writing rule file: {e}")

if __name__ == "__main__":
    create_technologies_rule() 