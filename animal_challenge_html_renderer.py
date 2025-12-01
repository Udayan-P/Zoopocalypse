import json
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess the Animal – {challenge_id}</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #111;
      color: #f5f5f5;
      margin: 0;
      padding: 2rem;
    }}
    .card {{
      max-width: 900px;
      margin: 0 auto;
      background: #181818;
      padding: 1.5rem 1.8rem;
      border-radius: 12px;
      box-shadow: 0 0 25px rgba(0,0,0,0.6);
    }}
    img {{
      max-width: 100%;
      border-radius: 10px;
      display: block;
      margin-bottom: 1.2rem;
    }}
    h1 {{
      margin-top: 0;
      margin-bottom: 1rem;
      font-size: 1.8rem;
    }}
    h2 {{
      margin-top: 1.3rem;
      margin-bottom: 0.6rem;
      font-size: 1.3rem;
    }}
    ul {{
      margin-top: 0.2rem;
    }}
    details {{
      margin: 0.3rem 0;
      padding: 0.4rem 0.6rem;
      background: #222;
      border-radius: 6px;
    }}
    summary {{
      cursor: pointer;
      font-weight: 600;
    }}
    .answer {{
      margin-top: 0.6rem;
      font-weight: 700;
      color: #ffd166;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Guess the Animal – {challenge_id}</h1>

    <img src="{image}" alt="Animal challenge image">

    <h2>Question</h2>
    <p>{question}</p>

    <h2>Options</h2>
    <ul>
      {options_html}
    </ul>

    <h2>Hints (for game master only)</h2>
    {hints_html}

    <h2>Answer (for game master only)</h2>
    <details>
      <summary>Reveal answer</summary>
      <p class="answer">{answer}</p>
    </details>
  </div>
</body>
</html>
"""


def render_challenge_to_html(json_path: str, html_path: str) -> None:
    """Read one challenge JSON file and write a standalone HTML page."""
    json_file = Path(json_path)
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Options as <li> elements
    options_html = "\n      ".join(
        f"<li>{opt}</li>" for opt in data["options"]
    )

    # Hints as collapsible <details> blocks
    hints_html_parts = []
    for i, hint in enumerate(data["hints"], start=1):
        hints_html_parts.append(
            f"<details><summary>Show Hint {i}</summary><p>{hint}</p></details>"
        )
    hints_html = "\n    ".join(hints_html_parts)

    html = HTML_TEMPLATE.format(
        challenge_id=data["challenge_id"],
        image=data["image"],          # e.g. "Dataset/Images/Cheetah.jpg"
        question=data["question"],
        options_html=options_html,
        hints_html=hints_html,
        answer=data["answer"],
    )

    out_file = Path(html_path)
    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote HTML challenge to {out_file}")


if __name__ == "__main__":
    
    render_challenge_to_html("generated_challenge.json", "animal_challenge.html")