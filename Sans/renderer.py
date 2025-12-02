import json
from pathlib import Path


def render_challenge(json_path: str, md_path: str) -> None:
    """
    Read a challenge JSON file and write a markdown file
    that can be used by the escape room game master.
    """
    json_file = Path(json_path)
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []

    # Title
    lines.append(f"# Guess the Animal – {data['challenge_id']}\n")

    # Image
    lines.append(f"![Animal image]({data['image']})\n")

    # Question
    lines.append(f"**Question:** {data['question']}\n")

    # Options
    lines.append("### Options\n")
    for opt in data["options"]:
        lines.append(f"- {opt}")
    lines.append("")  # blank line

    # Hints (for game master only)
    lines.append("---")
    lines.append("### Hints (for game master only)\n")
    for i, hint in enumerate(data["hints"], start=1):
        lines.append(f"- Hint {i}: {hint}")
    lines.append("")

    # Answer (for game master only)
    lines.append("---")
    lines.append("### Answer (for game master only)\n")
    lines.append(f"- **Correct answer:** {data['answer']}")
    lines.append("")

    markdown = "\n".join(lines)

    out_file = Path(md_path)
    out_file.write_text(markdown, encoding="utf-8")
    print(f"Wrote markdown to {out_file}")


if __name__ == "__main__":
    # Use the file you just generated
    render_challenge("generated_challenge.json", "generated_challenge.md")