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
    .points {{
      margin-bottom: 1rem;
      font-weight: 600;
    }}
    .options {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      margin-top: 0.4rem;
    }}
    .option-btn {{
      padding: 0.5rem 1.1rem;
      border-radius: 999px;
      border: 1px solid #444;
      background: #222;
      color: #f5f5f5;
      cursor: pointer;
      font-size: 0.95rem;
      transition: background 0.15s ease, transform 0.05s ease;
    }}
    .option-btn:hover {{
      background: #333;
      transform: translateY(-1px);
    }}
    .option-btn:active {{
      transform: translateY(0);
    }}
    .option-btn.correct {{
      background: #2d6a4f;
      border-color: #40916c;
    }}
    .option-btn.incorrect {{
      background: #6a2d2d;
      border-color: #c0392b;
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
    .message {{
      margin-top: 0.8rem;
      font-weight: 600;
      color: #ffd166;
    }}
  </style>
</head>
<body>
  <!-- data-answer holds the correct answer but is never shown directly -->
  <div class="card" id="challenge" data-answer="{answer}">
    <h1>Guess the Animal – {challenge_id}</h1>

    <img src="{image}" alt="Animal challenge image">

    <div class="points">
      Points remaining: <span id="points-value">3</span>
    </div>

    <h2>Question</h2>
    <p>{question}</p>

    <h2>Options</h2>
    <div class="options">
      {options_html}
    </div>

    <h2>Hints</h2>
    {hints_html}

    <div class="message" id="message-area"></div>
  </div>

  <script>
    // Points / hints logic
    let points = 3;
    const pointsSpan = document.getElementById("points-value");
    const messageArea = document.getElementById("message-area");
    const hintDetails = document.querySelectorAll("details.hint");

    hintDetails.forEach((detailsEl) => {{
      const summary = detailsEl.querySelector("summary");
      detailsEl.dataset.used = "false";

      summary.addEventListener("click", () => {{
        // Only deduct a point the FIRST time this hint is opened
        if (detailsEl.dataset.used === "true") {{
          return;
        }}
        detailsEl.dataset.used = "true";

        if (points > 0) {{
          points -= 1;
          pointsSpan.textContent = points;
        }}

        if (points <= 0) {{
          points = 0;
          pointsSpan.textContent = points;
          messageArea.textContent =
            "You have used all your hints. Restarting with a new animal...";
          restartChallenge();
        }}
      }});
    }});

    // Option button logic
    const challengeCard = document.getElementById("challenge");
    const correctAnswer = challengeCard.dataset.answer;
    const optionButtons = document.querySelectorAll(".option-btn");

    optionButtons.forEach((btn) => {{
      btn.addEventListener("click", () => {{
        // Clear previous visual state
        optionButtons.forEach((b) => {{
          b.classList.remove("correct", "incorrect");
        }});

        const chosen = btn.dataset.option;

        if (chosen === correctAnswer) {{
          btn.classList.add("correct");
          messageArea.textContent = "Correct! Well done.";
        }} else {{
          btn.classList.add("incorrect");
          messageArea.textContent = "Not quite. Try again or use a hint.";

          // Deduct 1 point for choosing a wrong option
          if (points > 0) {{
            points -= 1;
            pointsSpan.textContent = points;
          }}

          // If points reach 0, restart with a new animal
          if (points <= 0) {{
            points = 0;
            pointsSpan.textContent = points;
            messageArea.textContent =
              "You have used all your points. Restarting with a new animal...";
            restartChallenge();
            //need to either edit in pipeline or..mulitple html pages??
          }}
        }}
      }});
    }});

    // When points reach 0, move to the next animal challenge.
    // In the full escape-room game, the group can update this function
    // to actually load the next challenge's HTML page.
    function restartChallenge() {{
      // TODO: in the full group game, this should trigger a *new* animal challenge
      // (e.g. by navigating to a different HTML file or by loading new data).
      // For now, it simply reloads this page so the same template can be reused.
      window.location.reload();
      // Example for later:
      // window.location.href = "animal_challenge_002.html";
      // other options i can try ???
    }}
  </script>
</body>
</html>
"""


def render_challenge_to_html(json_path: str, html_path: str) -> None:
    """Read one challenge JSON file and write a standalone interactive HTML page."""
    json_file = Path(json_path)
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Options aree clickable buttons
    options_html = "\n      ".join(
        f'<button class="option-btn" data-option="{opt}">{opt}</button>'
        for opt in data["options"]
    )

    # Hints as <details> blocks with a 'hint' class so JS can hook into them
    hints_html_parts = []
    for i, hint in enumerate(data["hints"], start=1):
        hints_html_parts.append(
            f'<details class="hint"><summary>Show Hint {i}</summary><p>{hint}</p></details>'
        )
    hints_html = "\n    ".join(hints_html_parts)

    html = HTML_TEMPLATE.format(
        challenge_id=data["challenge_id"],
        image=data["image"],          # e.g. "Dataset/Images/Cheetah.jpg"
        question=data["question"],
        options_html=options_html,
        hints_html=hints_html,
        answer=data["answer"],        # stored only in data-answer, never shown
    )

    out_file = Path(html_path)
    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote HTML challenge to {out_file}")


if __name__ == "__main__":
    render_challenge_to_html("generated_challenge.json", "animal_challenge.html")