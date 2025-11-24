#!/usr/bin/env python3
"""
Feature Challenge Renderer 

"""

import json
import sys


def load_json(path):
    """Load JSON and do basic validation."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        print("Error reading JSON.")
        sys.exit(1)

    return data


def group_by_category(attributes):
    """Group attributes based on category."""
    grouped = {}
    for attr in attributes:
        cat = attr.get("category", "Other")
        grouped.setdefault(cat, []).append(attr)
    return grouped


def build_md_skeleton(data):
    """Create the outline of the markdown document without censoring yet."""

    md = []

    # Header
    md.append("# Feature Challenge: Identify the Animal\n\n")

    # Sections (still empty placeholders)
    md.append("## Instructions\nTo be completed.\n\n")
    md.append("## Rules\nTo be completed.\n\n")
    md.append("## Challenge\nSpecies: [CENSORED]\n\n")

    grouped = group_by_category(data["attributes"])

    for cat, items in grouped.items():
        md.append(f"### {cat}\n")
        for attr in items:
            md.append(f"- **{attr['label']}:** {attr['value']}\n")
        md.append("\n")

    return "".join(md)


def main():
    if len(sys.argv) < 3:
        print("Usage: python feature_challenge_renderer.py <input.json> <output.md>")
        sys.exit(1)

    data = load_json(sys.argv[1])
    md_output = build_md_skeleton(data)

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(md_output)

    print("✓ Markdown skeleton generated.")


if __name__ == "__main__":
    main()
