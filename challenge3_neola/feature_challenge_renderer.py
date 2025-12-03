#!/usr/bin/env python3

import json
import sys
import random
from pathlib import Path
import os

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

def build_hint_link(stage, attempts, base):
    return f"../stage_{stage}/{base}_hint{stage}_a{attempts}.html"

def build_wrong_link(stage, attempts, base):
    return f"../wrong/{base}_wrong_hint{stage}_a{attempts}.html"

def build_fail_link(base):
    return f"../fail/{base}_fail.html"

def build_answer_link(base):
    return f"../answer/{base}_answer.html"

def build_mcq_section(correct, base, stage, attempts, max_attempts):
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
            link = build_answer_link(base)
        else:
            next_attempt = attempts + 1
            if next_attempt >= max_attempts:
                link = build_fail_link(base)
            else:
                link = build_wrong_link(stage, next_attempt, base)
        out.append(f'    <a class="mcq-card" href="{link}">{opt}</a>\n')

    out.append("</div>\n\n")
    return "".join(out)

def main_menu_button():
    return (
        '<a class="back-main" href="../../../game.html">← Main Menu</a>\n'
        '<style>'
        '.back-main {'
        'display:inline-block;'
        'padding:8px 16px;'
        'background:#3266d6;'
        'color:white !important;'
        'text-decoration:none;'
        'font-size:16px;'
        'border-radius:8px;'
        'font-weight:600;'
        'position:absolute;'
        'top:20px;'
        'left:20px;'
        'z-index:9999;'
        'box-shadow:0 2px 4px rgba(0,0,0,0.15);'
        '}'
        '.back-main:hover{background:#2854b8;}'
        '</style>\n\n'
    )

def ai_hint_block(ai_text):
    if not ai_text:
        return ""

    return (
        "<div id='ai_hint_box' style='display:none; margin:20px auto;"
        "padding:16px; background:#e0f2fe; border-left:4px solid #0ea5e9;"
        "border-radius:10px; max-width:600px; font-size:1rem;'>"
        f"💡 {ai_text}"
        "</div>\n\n"
        "<script>"
        "function toggle_ai_hint(){"
        "var b=document.getElementById('ai_hint_box');"
        "b.style.display=b.style.display==='none'?'block':'none';"
        "}"
        "</script>"
    )

def render_state_md(data, initial_indices, remaining_order, stage, attempts, base, max_stage, max_attempts):
    attributes = data["attributes"]
    correct_animal = data["animal"]
    ai_hint = data.get("ai_hint_seed", "")

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
    md.append(main_menu_button())
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
    md.append(
        f"<p style='text-align:center;'>"
        f"<strong>Hints Remaining:</strong> {hints_remaining} | "
        f"<strong>Wrong Attempts:</strong> {attempts}/{max_attempts}"
        "</p>\n\n"
    )

    md.append(build_mcq_section(correct_animal, base, stage, attempts, max_attempts))

    links = []
    links.append(f"[Try Again]({build_hint_link(stage, attempts, base)})")

    if stage < max_stage:
        links.append(f"[Reveal Next Hint]({build_hint_link(stage+1, attempts, base)})")

    links.append(f"[Reveal Answer]({build_answer_link(base)})")

    if ai_hint:
        links.append("[AI Hint](javascript:toggle_ai_hint())")

    md.append("\n" + " | ".join(links) + "\n\n")

    if ai_hint:
        md.append(ai_hint_block(ai_hint))

    return "".join(md)

def render_wrong_page(data, base, stage, attempts, max_attempts):
    ai_hint = data.get("ai_hint_seed", "")
    md = []
    md.append(main_menu_button())
    md.append("# Wrong Answer\n\n")
    md.append(
        f"You have **{max_attempts - attempts}** attempts remaining.\n\n"
    )

    md.append(f"[Try Again]({build_hint_link(stage, attempts, base)}) | ")
    md.append(f"[Reveal Answer]({build_answer_link(base)})\n\n")

    if ai_hint:
        md.append("[AI Hint](javascript:toggle_ai_hint())\n\n")
        md.append(ai_hint_block(ai_hint))

    return "".join(md)

def render_answer_page(data, base, max_stage, initial_indices, remaining_order):
    ai_hint = data.get("ai_hint_seed", "")
    md = []

    md.append(main_menu_button())
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

    md.append(f"[Play Again from Start]({build_hint_link(0,0,base)})\n\n")

    if ai_hint:
        md.append("[AI Hint](javascript:toggle_ai_hint())\n\n")
        md.append(ai_hint_block(ai_hint))

    return "".join(md)

def render_fail_page(data, base):
    ai_hint = data.get("ai_hint_seed", "")
    md = []

    md.append(main_menu_button())
    md.append("# Challenge Failed\n")
    md.append(f"The correct species was **{data['animal']}**.\n\n")

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

    md.append(f"[Try Again from Start]({build_hint_link(0,0,base)})\n\n")

    if ai_hint:
        md.append("[AI Hint](javascript:toggle_ai_hint())\n\n")
        md.append(ai_hint_block(ai_hint))

    return "".join(md)

def generate_multi_files(data, input_file, outdir):
    os.makedirs(outdir, exist_ok=True)

    base = Path(input_file).stem
    attributes = data["attributes"]
    num_attrs = len(attributes)

    max_stage = 3     
    
    max_attempts = 2  

    all_idx = list(range(num_attrs))
    random.shuffle(all_idx)

    initial_indices = set(all_idx[:min(5, num_attrs)])
    remaining_order = all_idx[min(5, num_attrs):]

    for stage in range(max_stage + 1):
        stage_dir = os.path.join(outdir, f"stage_{stage}")
        os.makedirs(stage_dir, exist_ok=True)

        for attempts in range(max_attempts):
            fname = f"{base}_hint{stage}_a{attempts}.md"
            out = os.path.join(stage_dir, fname)
            content = render_state_md(
                data, initial_indices, remaining_order,
                stage, attempts, base, max_stage, max_attempts
            )
            with open(out, "w", encoding="utf-8") as f:
                f.write(content)

    wrong_dir = os.path.join(outdir, "wrong")
    os.makedirs(wrong_dir, exist_ok=True)

    for stage in range(max_stage + 1):
        for attempts in range(1, max_attempts):
            fname = f"{base}_wrong_hint{stage}_a{attempts}.md"
            out = os.path.join(wrong_dir, fname)
            content = render_wrong_page(data, base, stage, attempts, max_attempts)
            with open(out, "w", encoding="utf-8") as f:
                f.write(content)

    answer_dir = os.path.join(outdir, "answer")
    os.makedirs(answer_dir, exist_ok=True)
    ans = os.path.join(answer_dir, f"{base}_answer.md")
    with open(ans, "w", encoding="utf-8") as f:
        f.write(render_answer_page(data, base, max_stage, initial_indices, remaining_order))

    fail_dir = os.path.join(outdir, "fail")
    os.makedirs(fail_dir, exist_ok=True)
    fail = os.path.join(fail_dir, f"{base}_fail.md")
    with open(fail, "w", encoding="utf-8") as f:
        f.write(render_fail_page(data, base))

def main():
    if len(sys.argv) < 4:
        print("Usage: python feature_challenge_renderer.py input.json --multi --outdir <folder>")
        sys.exit(1)

    data = load_json(sys.argv[1])

    if "--multi" not in sys.argv:
        print("Error: use --multi")
        sys.exit(1)

    if "--outdir" in sys.argv:
        outdir = sys.argv[sys.argv.index("--outdir") + 1]
    else:
        outdir = "challenge3_neola/pages"

    generate_multi_files(data, sys.argv[1], outdir)

if __name__ == "__main__":
    main()
