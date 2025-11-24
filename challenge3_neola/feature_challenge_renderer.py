#!/usr/bin/env python3
"""
Feature Challenge Renderer Final

"""

import json
import sys
from pathlib import Path


def load_json(path):
    """Load JSON and do basic validation."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: The input JSON file was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Could not decode JSON. Please check formatting.")
        sys.exit(1)

    # Required fields check
    needed = ["challenge_type", "animal", "attributes", "initial_hints", "max_additional_hints"]
    for field in needed:
        if field not in data:
            print(f"Error: Missing required field '{field}' in JSON.")
            sys.exit(1)

    if data["challenge_type"] != "feature_challenge":
        print("Error: challenge_type must be 'feature_challenge'.")
        sys.exit(1)

    return data


def group_by_category(attributes):
    """Put attributes into category groups for cleaner printing."""
    grouped = {}
    for attr in attributes:
        cat = attr["category"]
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(attr)
    return grouped


def render_to_markdown(data):
    """Convert JSON challenge into a Markdown string."""
    attributes = data["attributes"]
    initial = set(data["initial_hints"])

    # This ordering is manually written so categories appear in a nicer order
    # (not alphabetical).
    category_order = [
        "Descriptive Profile",
        "Geographic & Conservation",
        "Diet",
        "Physical Features",
        "Biological Traits",
        "Habitat & Environment"
    ]

    grouped = group_by_category(attributes)

    md = []

    # Title
    md.append("# Feature Challenge: Identify the Animal\n")

    # Instructions
    md.append("## Instructions\n")
    md.append("You are given several attribute categories describing a hidden animal.\n")
    md.append("Some attributes are shown, and the rest are censored. You may reveal\n")
    md.append("additional hints if needed.\n\n")

    # Rules
    md.append("## Rules\n")
    md.append("1. Three attributes are revealed from the start.\n")
    md.append(f"2. You can unlock up to **{data['max_additional_hints']}** more hints.\n")
    md.append("3. Guess the animal at any point to complete the challenge.\n\n")

    # Challenge section
    md.append("## Challenge\n")
    md.append("**Species:** `[CENSORED]`\n")

    # Display attribute categories
    md.append("\n---\n")

    for cat in category_order:
        if cat in grouped:
            md.append(f"### {cat}\n")
            for idx, attr in enumerate(attributes):
                if attr["category"] != cat:
                    continue

                label = attr["label"]
                value = attr["value"]

                # Reveal or censor
                if idx in initial:
                    md.append(f"- **{label}:** {value} *(initial hint)*\n")
                else:
                    md.append(f"- **{label}:** `[CENSORED]`\n")
            md.append("\n")

    # Hints section
    md.append("## Hints\n")
    md.append("These are the attributes that were revealed at the start:\n\n")

    for idx in data["initial_hints"]:
        attr = attributes[idx]
        md.append(f"- {attr['category']} → {attr['label']}: {attr['value']}\n")

    md.append(f"\n**Additional hints available:** {data['max_additional_hints']}\n")
    md.append("Each extra hint will reveal one censored attribute.\n\n")

    # Answer for facilitator
    md.append("## Answer\n")
    md.append(f"**Correct Animal:** {data['animal']}\n\n")

    # Full uncensored list (facilitator section)
    md.append("### Complete Attribute List\n")
    for cat in category_order:
        if cat in grouped:
            md.append(f"\n**{cat}:**\n")
            for attr in grouped[cat]:
                md.append(f"- {attr['label']}: {attr['value']}\n")

    return "".join(md)


def main():
    if len(sys.argv) < 3:
        print("Usage: python feature_challenge_renderer.py <input.json> <output.md>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = load_json(input_file)
    result = render_to_markdown(data)

    # Write to file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Markdown file created: {output_file}")
    except Exception as e:
        print("Error writing markdown output:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
