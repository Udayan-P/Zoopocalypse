import json
from pathlib import Path

from generator import load_dataset, make_single_challenge
from animal_challenge_html_renderer import render_challenge_to_html


def main():
    # 1) build challenge from dataset
    df = load_dataset()
    challenge = make_single_challenge(df)

    # 2) save JSON
    json_path = Path("generated_challenge.json")
    json_path.write_text(json.dumps(challenge, indent=4), encoding="utf-8")
    print(f"Saved challenge JSON to {json_path}")

    # 3) render HTML
    render_challenge_to_html(str(json_path), "animal_challenge.html")


if __name__ == "__main__":
    main()