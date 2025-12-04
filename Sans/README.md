# Zoopocalypse Challenge 1

🐾 Guess the Animal From the Blurred Picture 

A JSON-Driven Image-Guessing Puzzle with Blurred Images, Hints & Dynamic HTML Rendering

# Overview

This challenge presents the player with a blurred image of an animal.
The player must identify the correct animal by either:
	•	Revealing hints, or
	•	Gradually unblurring the image

Each action costs 1 point, so the player must think strategically.
The challenge ends when the user either guesses correctly or runs out of points.





📁 Files Included

File	Description
generator.py	Loads dataset, generates JSON challenge object.
animal_challenge_pipeline.py	Runs the pipeline: generate JSON → produce HTML.
animal_challenge.html	Final rendered interactive challenge.
generated_challenge.json	Example JSON output for one challenge instance.
animal_challenge_html_renderer.py	Converts JSON → interactive HTML puzzle.

** please do note, js only used in minimal as inlined script within htmls for aesthetics only, but never on it's own as a .js file **




🐆 JSON Structure

Each challenge is generated in the following format:

```

{
  "challenge_id": "animal_001",
  "image": "Dataset/Images/Seal.jpg",
  "question": "Which animal is shown in this picture?",
  "options": ["seal", "tortoise", "lion", "mole"],
  "answer": "seal",
  "hints": [
    "This animal is primarily a carnivore.",
    "It typically lives in cold coastal waters.",
    "Its predators include polar bears and orcas.",
    "It belongs to the Phocidae family."
  ]
}
```

This JSON drives the entire challenge and is used by the HTML renderer.



🦓 Gameplay Logic
	•	The image begins fully blurred.
	•	Player may choose to:
	•	Reveal a hint → costs 1 point
	•	Reveal more of the image → costs 1 point
	•	Choosing the correct animal:
	•	Stops the game
	•	Reveals the image instantly
	•	Points reaching 0:
	•	Ends the challenge
	•	Auto-reloads a new random animal



🦘 Hint Generation + Unblurring picture option

Hints are created using real biological attributes from the dataset:
	•	Diet
	•	Habitat
	•	Predators
	•	Family
	•	Conservation status

They progress from vague → specific to control difficulty.

If the dataset lacks information, generic fallback hints are used.
Picture also start off blurry, so with a click of the unblur button, users can guess better but it costs them 1 point.



🦧 Pipeline Summary

Running the pipeline:

python Sans/animal_challenge_pipeline.py

Steps performed:
	1.	Load dataset
	2.	Randomly select animal
	3.	Generate JSON file
	4.	Render final animal_challenge.html
	5.	Output playable challenge

The root game.py will also run all team pipelines and open the browser automatically.



🦥 Features
	•	Dynamic blur reduction
	•	Interactive hint toggles
	•	Automatic point deduction
	•	Auto-generated HTML
	•	Dataset-driven difficulty
	•	Self-contained and reproducible pipeline



 ✔ Status

This challenge has been implemented, tested, and runs successfully in:
	•	Local environment
	•	Root game.py pipeline
	•	JSON generation and HTML rendering

Fully compliant with module requirements.

