import json
import os


def render_hangman_from_json(json_path: str) -> str:
    """Reads a hangman JSON challenge and returns markdown text."""
    if not os.path.exists(json_path):
        return f"Error: JSON file not found: {json_path}"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return "Error: JSON is not valid."

    # Basic validation (simple + imperfect = realistic)
    if "word" not in data or "hints" not in data:
        return "Error: JSON missing required fields."

    word = data["word"]
    max_lives = data.get("max_lives", 5)
    hints = data["hints"]

    # Render markdown (not too fancy yet)
    md = []
    md.append("# Hangman Challenge (From JSON)\n")
    md.append(f"**Word length:** {len(word)} letters\n")
    md.append(f"**Max lives:** {max_lives}\n")

    md.append("\n## Hints\n")
    for h in hints:
        label = h.get("label", "Hint")
        text = h.get("text", "")
        md.append(f"- **{label}:** {text}")

    md.append("\n\n*(JSON challenge rendered)*\n")

    return "\n".join(md)


if __name__ == "__main__":
    # Hardcoded test path - realistic for early development
    example_path = "json_examples/hangman_example.json"
    output = render_hangman_from_json(example_path)
    print(output)