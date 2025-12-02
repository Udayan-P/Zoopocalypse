import json
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess the Animal – Challenge 1</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #111;
      color: #f5f5f5;
      margin: 0;
      padding: 2rem;
    }}
    .card {{
      position: relative;
      max-width: 900px;
      margin: 0 auto;
      background: #181818;
      padding: 1.5rem 1.8rem;
      border-radius: 12px;
      box-shadow: 0 0 25px rgba(0,0,0,0.6);
      overflow: hidden;
    }}
    .animal-image {{
      max-width: 100%;
      border-radius: 10px;
      display: block;
      margin-bottom: 1.2rem;
      filter: blur(12px);
      opacity: 0.4;
      transition: filter 0.25s ease, opacity 0.25s ease;
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
    .option-btn:disabled {{
      cursor: default;
      opacity: 0.6;
    }}
    .hints-grid {{
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      margin-top: 0.4rem;
    }}

    details.hint {{
      margin: 0;
      padding: 0.6rem 0.8rem;
      background: radial-gradient(circle at top left, #222 0, #181818 45%, #121212 100%);
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 0 12px rgba(0, 0, 0, 0.5);
    }}

    details.hint[open] {{
      border-color: #ffd16644;
      box-shadow: 0 0 18px rgba(255, 209, 102, 0.25);
    }}

    summary {{
      cursor: pointer;
      font-weight: 600;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.1rem 0;
    }}

    summary::-webkit-details-marker {{
      display: none;
    }}

    .hint-index {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 1.8rem;
      height: 1.8rem;
      border-radius: 999px;
      background: rgba(255, 209, 102, 0.12);
      border: 1px solid rgba(255, 209, 102, 0.4);
      font-size: 0.85rem;
      font-weight: 700;
      color: #ffd166;
      flex-shrink: 0;
    }}

    details.hint p {{
      margin: 0.3rem 0 0;
      font-size: 0.95rem;
      color: #e8e8e8;
      line-height: 1.4;
    }}
    .message {{
      margin-top: 0.8rem;
      font-weight: 600;
      color: #ffd166;
      padding: 0.5rem 0.8rem;
      border-radius: 8px;
      background: rgba(255, 209, 102, 0.06);
      border: 1px solid rgba(255, 209, 102, 0.22);
    }}
    
    .instructions {{
      background: rgba(255,255,255,0.05);
      border: 2px solid rgba(255,255,255,0.1);
      padding: 1rem 1.2rem;
      border-radius: 10px;
      margin-bottom: 1.5rem;
      backdrop-filter: blur(4px);
    }}

    .instructions h3 {{
      margin: 0 0 0.4rem 0;
      font-size: 1.2rem;
      font-weight: 600;
      color: #ffd166;
    }}

    .instructions p {{
      margin: 0;
      line-height: 1.4;
      font-size: 0.95rem;
      color: #f0f0f0;
    }}
  </style>
</head>
<body>
  
  <div class="instructions">
    <h3>🔍 How to Play</h3>
    <p>
      The image begins blurred. Use hints to make the picture clearer — 
      but each hint costs 1 point!  
      Choose the correct animal before your points run out.
    </p>
  </div> 
  
  <div class="card" id="challenge" data-answer="{answer}">

    <h1>Guess the Animal – Challenge 1</h1>

    <img
      id="animal-image"
      class="animal-image"
      src="{image}"
      alt="Animal challenge image"
    >

    <div class="points">
      Points remaining: <span id="points-value">3</span>
    </div>

    <div class="message" id="message-area"></div>

    <h2>Question</h2>
    <p>{question}</p>

    <h2>Options</h2>
    <div class="options">
      {options_html}
    </div>

    <h2>Hints</h2>
    <div class="hints-grid">
      {hints_html}
    </div>

  </div>

  <script>
    // ------ BLUR / CLARITY LOGIC ------
    let blurLevel = 18;
    const minBlur = 0;
    const blurStep = 2;
    const img = document.getElementById("animal-image");
    let solved = false;

    function updateImageBlur() {{
      const effectiveBlur = Math.max(minBlur, blurLevel);
      img.style.filter = "blur(" + effectiveBlur + "px)";
      const t = 1 - (effectiveBlur / 12);
      img.style.opacity = 0.4 + t * 0.6;
    }}

    updateImageBlur();

    // ------ POINTS + HINTS ------
    let points = 3;
    const pointsSpan = document.getElementById("points-value");
    const messageArea = document.getElementById("message-area");
    const hintDetails = document.querySelectorAll("details.hint");

    hintDetails.forEach((detailsEl) => {{
      const summary = detailsEl.querySelector("summary");
      detailsEl.dataset.used = "false";

      summary.addEventListener("click", () => {{
        if (solved || detailsEl.dataset.used === "true") {{
          return;
        }}
        detailsEl.dataset.used = "true";

        if (points > 0) {{
          points -= 1;
          pointsSpan.textContent = points;
        }}

        blurLevel -= blurStep;
        updateImageBlur();

        if (points <= 0) {{
          points = 0;
          pointsSpan.textContent = points;
          messageArea.textContent =
            "You have used all your hints. Restarting with a new animal...";
          restartChallenge();
        }}
      }});
    }});

    // ------ OPTIONS (GUESSING) ------
    const challengeCard = document.getElementById("challenge");
    const correctAnswer = challengeCard.dataset.answer;
    const optionButtons = document.querySelectorAll(".option-btn");

    optionButtons.forEach((btn) => {{
      btn.addEventListener("click", () => {{
        if (solved) {{
          return;
        }}
        optionButtons.forEach((b) => {{
          b.classList.remove("correct", "incorrect");
        }});

        const chosen = btn.dataset.option;

        if (chosen === correctAnswer) {{
          btn.classList.add("correct");
          messageArea.textContent = "Correct! Well done.";

          // Reveal the image instantly (no blur, full opacity)
          blurLevel = 0;
          img.style.filter = "blur(0px)";
          img.style.opacity = "1";

          // NEED TO lock the challenge: mark as solved and disable all options
          //lowk why does the hints still show after points = 0 , NEED FIX!
          solved = true;
          optionButtons.forEach((b) => {{
            b.disabled = true;
          }});

        }} else {{
          btn.classList.add("incorrect");
          messageArea.textContent = "Not quite. Try again or use a hint.";

          if (points > 0) {{
            points -= 1;
            pointsSpan.textContent = points;
          }}

          if (points <= 0) {{
            points = 0;
            pointsSpan.textContent = points;
            messageArea.textContent =
              "You have used all your points. Restarting with a new animal...";
            restartChallenge();
          }}
        }}
      }});
    }});

    function restartChallenge() {{
      window.location.reload();
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

    options_html = "\n      ".join(
        f'<button class="option-btn" data-option="{opt}">{opt}</button>'
        for opt in data["options"]
    )

    hints_html_parts = []
    for i, hint in enumerate(data["hints"], start=1):
        hints_html_parts.append(
            f'<details class="hint">'
            f'<summary><span class="hint-index">{i}</span> Reveal Hint {i}</summary>'
            f'<p>{hint}</p>'
            f'</details>'
        )
    hints_html = "\n    ".join(hints_html_parts)

    html = HTML_TEMPLATE.format(
        challenge_id=data["challenge_id"],
        image=data["image"],
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