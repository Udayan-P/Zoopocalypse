#!/usr/bin/env python3

import json
import sys
import random
from pathlib import Path
import os

OUTPUT_DIR = "pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Error loading JSON.")
        sys.exit(1)

    required = ["challenge_type", "animal", "attributes", "initial_hints", "max_additional_hints"]
    for r in required:
        if r not in data:
            print(f"Missing field: {r}")
            sys.exit(1)
    return data


def group_by_category(attributes):
    grouped = {}
    for attr in attributes:
        grouped.setdefault(attr["category"], []).append(attr)
    return grouped


def build_mcq_section(correct, file_prefix, stage, attempts, max_attempts):
    distractors = [
        "Lion","Beaver","Otter","Kangaroo","Wombat","Koala","Pangolin","Leopard",
        "Serval","Cheetah","Fox","Wolf","Jaguar","Ocelot","Hedgehog",
        "Capybara","Badger","Red Panda"
    ]
    distractors = [d for d in distractors if d.lower() != correct.lower()]
    random.shuffle(distractors)
    options = distractors[:7]
    all_opts = [correct] + options
    random.shuffle(all_opts)

    out = []
    out.append("## Choose the Species\n\n")
    out.append('<div class="mcq-grid">\n')

    for opt in all_opts:
        if opt.lower() == correct.lower():
            link = f"{file_prefix}_answer.html"
        else:
            next_attempt = attempts + 1
            if next_attempt >= max_attempts:
                link = f"{file_prefix}_fail.html"
            else:
                link = f"{file_prefix}_wrong_hint{stage}_a{next_attempt}.html"
        out.append(f'    <a class="mcq-card" href="{link}">{opt}</a>\n')

    out.append("</div>\n\n")
    return "".join(out)


def render_state_md(data, initial_indices, remaining_order, stage, attempts, file_prefix, max_stage, max_attempts):
    attributes = data["attributes"]
    correct_animal = data["animal"]

    extra_hints = min(stage, max_stage, len(remaining_order))
    extra_indices = set(remaining_order[:extra_hints])
    grouped = group_by_category(attributes)

    order = [
        "Descriptive Profile",
        "Geographic & Conservation",
        "Diet",
        "Physical Features",
        "Biological Traits",
        "Habitat & Environment"
    ]

    md = []
    md.append("# Feature Challenge: Identify the Animal\n")
    md.append("## Instructions\n")
    md.append("Use the revealed attributes to guess the hidden species.\n")
    md.append(f"You have up to {max_attempts} wrong attempts before failure.\n\n")
    md.append("---\n")
    md.append("## Species\n")
    md.append("### `[CENSORED]`\n")
    md.append("---\n\n")

    for cat in order:
        cat_attrs = [(idx, a) for idx, a in enumerate(attributes) if a["category"] == cat]
        if not cat_attrs:
            continue
        md.append(f"### {cat}\n")
        for idx, attr in cat_attrs:
            label = attr["label"]
            value = attr["value"]
            if idx in initial_indices:
                md.append(f"- **{label}:** {value} (revealed)\n")
            elif idx in extra_indices:
                md.append(f"- **{label}:** {value} (hint)\n")
            else:
                md.append(f"- **{label}:** `[CENSORED]`\n")
        md.append("\n")

    hints_remaining = max(0, max_stage - stage)
    attempts_left = max(0, max_attempts - attempts)

    md.append(
        f"<p style='text-align:center; font-size:1.05rem;'>"
        f"<span style='color:#166534; font-weight:700;'>Hints Remaining: {hints_remaining}</span>"
        f" &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<span style='font-weight:600;'>Wrong Attempts: {attempts} / {max_attempts}</span>"
        f"</p>\n\n"
    )

    md.append(build_mcq_section(correct_animal, file_prefix, stage, attempts, max_attempts))

    links = []
    links.append(f"[Try Again]({file_prefix}_hint{stage}_a{attempts}.html)")
    if stage < max_stage:
        links.append(f"[Reveal Next Hint]({file_prefix}_hint{stage+1}_a{attempts}.html)")
    links.append(f"[Reveal Answer]({file_prefix}_answer.html)")

    md.append("\n" + " | ".join(links) + "\n")
    return "".join(md)


def render_wrong_page(data, file_prefix, stage, attempts, max_attempts):
    attempts_left = max(0, max_attempts - attempts)
    md = []
    md.append("# Wrong Answer\n\n")
    md.append(
        "<div class=\"status-card status-card--wrong\">"
        "<h2 class=\"status-title\">Wrong Answer</h2>"
        f"<p class=\"status-text\">Try again! You have <strong>{attempts_left}</strong> attempts remaining.</p>"
        "</div>\n\n"
    )
    links = []
    links.append(f"[Try Again]({file_prefix}_hint{stage}_a{attempts}.html)")
    links.append(f"[Reveal Answer]({file_prefix}_answer.html)")
    md.append(" | ".join(links) + "\n")
    return "".join(md)


def render_answer_page(data, file_prefix, max_stage, initial_indices, remaining_order):
    md = []
    md.append("# Correct Answer\n")
    md.append(f"## The animal was: **{data['animal']}**\n")
    md.append("---\n\n")

    grouped = group_by_category(data["attributes"])
    order = [
        "Descriptive Profile","Geographic & Conservation","Diet",
        "Physical Features","Biological Traits","Habitat & Environment"
    ]

    for cat in order:
        if cat in grouped:
            md.append(f"### {cat}\n")
            for attr in grouped[cat]:
                md.append(f"- **{attr['label']}:** {attr['value']}\n")
            md.append("\n")

    md.append(f"[Play Again from Start]({file_prefix}_hint0_a0.html)\n")
    return "".join(md)


def render_fail_page(data, file_prefix):
    md = []
    md.append("# Challenge Failed\n")
    md.append("## You used all your attempts.\n\n")
    md.append(f"The correct species was: **{data['animal']}**.\n")
    md.append("---\n\n")

    grouped = group_by_category(data["attributes"])
    order = [
        "Descriptive Profile","Geographic & Conservation","Diet",
        "Physical Features","Biological Traits","Habitat & Environment"
    ]

    for cat in order:
        if cat in grouped:
            md.append(f"### {cat}\n")
            for attr in grouped[cat]:
                md.append(f"- **{attr['label']}:** {attr['value']}\n")
            md.append("\n")

    md.append(f"[Try Again from Start]({file_prefix}_hint0_a0.html)\n")
    return "".join(md)


def generate_multi_files(data, input_file):
    base = Path(input_file).stem
    attributes = data["attributes"]
    num_attrs = len(attributes)

    max_stage = data.get("max_additional_hints", 5)
    max_attempts = 3

    all_idx = list(range(num_attrs))
    random.shuffle(all_idx)

    initial_indices = set(all_idx[:min(5, num_attrs)])
    remaining_order = all_idx[min(5, num_attrs):]

    for stage in range(max_stage + 1):
        for attempts in range(max_attempts):
            filename = f"{base}_hint{stage}_a{attempts}.md"
            out_path = os.path.join(OUTPUT_DIR, filename)
            content = render_state_md(data, initial_indices, remaining_order, stage, attempts, base, max_stage, max_attempts)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Created", out_path)

    for stage in range(max_stage + 1):
        for attempts in range(1, max_attempts):
            filename = f"{base}_wrong_hint{stage}_a{attempts}.md"
            out_path = os.path.join(OUTPUT_DIR, filename)
            content = render_wrong_page(data, base, stage, attempts, max_attempts)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Created", out_path)

    ans_path = os.path.join(OUTPUT_DIR, f"{base}_answer.md")
    with open(ans_path, "w", encoding="utf-8") as f:
        f.write(render_answer_page(data, base, max_stage, initial_indices, remaining_order))

    fail_path = os.path.join(OUTPUT_DIR, f"{base}_fail.md")
    with open(fail_path, "w", encoding="utf-8") as f:
        f.write(render_fail_page(data, base))


def main():
    if len(sys.argv) < 2:
        print("Usage: python feature_challenge_renderer.py input.json --multi")
        sys.exit(1)
    data = load_json(sys.argv[1])
    if sys.argv[2] == "--multi":
        generate_multi_files(data, sys.argv[1])
    else:
        print("Error: use --multi")
        sys.exit(1)


if __name__ == "__main__":
    main()
