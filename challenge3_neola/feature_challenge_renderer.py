#!/usr/bin/env python3

import json
import sys
import random
from pathlib import Path

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: The input JSON file was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Could not decode JSON. Please check formatting.")
        sys.exit(1)

    needed = ["challenge_type", "animal", "attributes", "initial_hints", "max_additional_hints"]
    for field in needed:
        if field not in data:
            print(f"Error: Missing required field '{field}'.")
            sys.exit(1)

    return data

def group_by_category(attributes):
    grouped = {}
    for attr in attributes:
        grouped.setdefault(attr["category"], []).append(attr)
    return grouped

def build_mcq_section(correct_animal):
    distractors = [
        "Lion","Otter","Beaver","Wombat","Koala","Fox","Cheetah","Capybara",
        "Hedgehog","Red Panda","Jaguar"
    ]

    distractors = [d for d in distractors if d.lower() != correct_animal.lower()]
    random.shuffle(distractors)

    options = [correct_animal] + distractors[:3]
    random.shuffle(options)

    out = []
    out.append("## Guess the Animal\n")
    for opt in options:
        out.append(f"- {opt}\n")

    return "".join(out)

def render_to_markdown(data):
    attributes = data["attributes"]
    initial = set(data["initial_hints"])
    grouped = group_by_category(attributes)

    category_order = [
        "Descriptive Profile",
        "Geographic & Conservation",
        "Diet",
        "Physical Features",
        "Biological Traits",
        "Habitat & Environment"
    ]

    md = []
    md.append("# Feature Challenge: Identify the Animal\n\n")
    md.append("## Instructions\n")
    md.append("Use the revealed attributes to guess the hidden animal.\n\n")

    md.append("## Species\n`[CENSORED]`\n\n")
    md.append("---\n\n")

    for cat in category_order:
        if cat not in grouped:
            continue
        md.append(f"### {cat}\n")
        for idx, attr in enumerate(attributes):
            if attr["category"] != cat:
                continue
            if idx in initial:
                md.append(f"- **{attr['label']}**: {attr['value']} *(initial hint)*\n")
            else:
                md.append(f"- **{attr['label']}**: `[CENSORED]`\n")
        md.append("\n")

    md.append("## Revealed Hints\n")
    for idx in data["initial_hints"]:
        a = attributes[idx]
        md.append(f"- {a['category']} → {a['label']}: {a['value']}\n")

    md.append("\n")
    md.append(build_mcq_section(data["animal"]))
    md.append("\n")

    md.append("## Correct Answer\n")
    md.append(f"**{data['animal']}**\n")

    return "".join(md)

def main():
    if len(sys.argv) < 3:
        print("Usage: python renderer.py input.json output.md")
        sys.exit(1)

    data = load_json(sys.argv[1])
    out = render_to_markdown(data)

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(out)

if __name__ == "__main__":
    main()
