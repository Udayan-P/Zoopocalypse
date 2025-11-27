import json
from pathlib import Path
from typing import Dict, Any


def load_json(path: str) -> Dict[str, Any]:
    """
    Loads a JSON hangman challenge file.
    """
    with open(path, "r") as f:
        return json.load(f)


def render_markdown(challenge: Dict[str, Any]) -> str:
    """
    Convert a JSON hangman challenge into a markdown document.
    """

    word_display = " ".join("_" for _ in challenge["word"])
    hints_list = "\n".join([f"- **{h['label']}**: {h['text']}" for h in challenge["hints"]])

    md = f"""# Challenge 1: Hangman

Guess the animal before the zombies reach the monkey.

**Word:** {word_display}  
**Lives:** {challenge.get("max_lives", 5)}

## Hints
{hints_list}

## Dataset Metadata
- Dataset: {challenge["dataset_metadata"]["dataset_name"]}
- Row index: {challenge["dataset_metadata"]["row_index"]}
"""

    return md


def save_markdown(content: str, out_path: str):
    """
    Save markdown content to file.
    """
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with out_file.open("w", encoding="utf-8") as f:
        f.write(content)


def render_and_save(input_json: str, out_md: str):
    """
    High-level helper that loads JSON, renders markdown,
    and writes it to the output folder.
    """
    challenge = load_json(input_json)
    md = render_markdown(challenge)
    save_markdown(md, out_md)
    print(f"Markdown written to: {out_md}")


if __name__ == "__main__":
    # Render hand-coded example JSON
    render_and_save(
        "json_examples/hangman_example.json",
        "output/hangman_example.md"
    )

    # Render generated JSON if it exists
    gen_json = Path("json_examples/generated_hangman.json")
    if gen_json.exists():
        render_and_save(
            "json_examples/generated_hangman.json",
            "output/hangman_generated.md"
        )
    else:
        print("Note: No generated_hangman.json found. Run the generator first.")