#!/usr/bin/env python3

import json
import sys
import random
from pathlib import Path

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Error: Could not load JSON.")
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
        "Lion","Otter","Beaver","Wombat","Koala","Fox","Cheetah",
        "Capybara","Hedgehog","Red Panda","Jaguar"
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

def render_to_markdown(data, stage):
    attributes = data["attributes"]
    initial = set(data["initial_hints"])

    all_indices = list(range(len(attributes)))
    random.shuffle(all_indices)

    reveal_queue = [i for i in all_indices if i not in initial]

    extra_revealed = set(reveal_queue[:stage])

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

    md.append(f"### Current Hint Stage: {stage}\n\n")

    md.append("## Species\n`[CENSORED]`\n\n")
    md.append("---\n\n")

    for cat in category_order:
        if cat not in grouped:
            continue
        md.append(f"### {cat}\n")
        for idx, attr in enumerate(attributes):
            if attr["category"] != cat:
                continue

            if idx in initial or idx in extra_revealed:
                md.append(f"- **{attr['label']}**: {attr['value']}\n")
            else:
                md.append(f"- **{attr['label']}**: `[CENSORED]`\n")

        md.append("\n")

    md.append("## Revealed Initial Hints\n")
    for idx in data["initial_hints"]:
        a = attributes[idx]
        md.append(f"- {a['category']} → {a['label']}: {a['value']}\n")

    md.append("\n")
    md.append("## Additional Hints\n")
    for idx in extra_revealed:
        a = attributes[idx]
        md.append(f"- {a['category']} → {a['label']}: {a['value']}\n")

    md.append("\n")
    md.append(build_mcq_section(data["animal"]))
    md.append("\n")

    md.append("## Correct Answer\n")
    md.append(f"**{data['animal']}**\n")

    return "".join(md)

def main():
    if len(sys.argv) < 4:
        print("Usage: python renderer.py input.json output.md stage")
        sys.exit(1)

    stage = int(sys.argv[3])

    data = load_json(sys.argv[1])
    out = render_to_markdown(data, stage)

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(out)

if __name__ == "__main__":
    main()
