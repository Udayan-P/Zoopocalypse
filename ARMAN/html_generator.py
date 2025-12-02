import os

print("Helloooo")
def generate_patterns(randomized_list, correct_order):
    patterns = []
    for animal in randomized_list:
        
        rank = correct_order.index(animal) + 1
        patterns.append(rank)
    return patterns

MD_FILE = "ARMAN/challenge1.md"
OUT_DIR = "ARMAN/html"

os.makedirs(OUT_DIR, exist_ok=True)

animals = []
correct_order = []
pattern = []

with open(MD_FILE, "r") as f:
    lines = [line.strip() for line in f]

mode = None 

for line in lines:

    if "Sort the animals" in line:
        start = line.find("by their") + len("by their ")
        end = line.find(", from")
        challenge_type = line[start:end].strip()
        challenge_type = challenge_type.replace("**", "")
        continue

    elif line.startswith("## Animals"):
        mode = "animals"
        continue
    elif line.startswith("## Correct Order"):
        mode = "correct"
        continue

    if mode == "animals":
        if line.startswith("- **") and line.endswith("**"):
            animal = line[4:-2]
            animals.insert(0, animal)

    elif mode == "correct":
        if "→" in line:
            correct_order = [x.strip() for x in line.split("→")]

pattern = generate_patterns(animals, correct_order)

challenge_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Animal Sorting Challenge</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<a class="back-main" href="../../game.html">← Main Menu</a>

<h1>Animal Sorting Challenge</h1>
<p>Sort the animals by <strong>smallest → largest</strong> weight.</p>

<div class="animal-list">
"""

for i, a in enumerate(animals, start=1):
    challenge_html += f"    <p>{i}. {a}</p>\n"

challenge_html += """
</div>

<h3>Your Answer:</h3>

<form action="results.html" method="get">
    <div class="inputs">
"""

#for i in range(1, len(animals) + 1):
#    challenge_html += (
#        f'        <input type="text" placeholder="Enter only the number" required>\n'
#    )

for i, p in enumerate(pattern, start=1):
    challenge_html += f'<input type="text" placeholder="Number Only" pattern="{p}" required>\n'


challenge_html += """    </div>
    <button type="submit">Check Answer →</button>
</form>

<a href="hints.html" class="hint-link">Need Hints?</a>

</body>
</html>
"""

with open(f"{OUT_DIR}/challenge.html", "w") as f:
    f.write(challenge_html)

image_map = {
    "Platypus": "images/platypus.jpg",
    "Emperor Penguin": "images/emperor_penguin.jpg",
    "Western Gorilla": "images/western_gorilla.jpg",
    "African Lion": "images/african_lion.jpg",
    "Asian Elephant": "images/asian_elephant.jpg"
}

hints_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hints</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<a class="back-main" href="../../game.html">← Main Menu</a>

<h1>Hints</h1>
<p>Here are the animals with images.</p>

<div class="hints-grid">
"""

for animal in animals:
    img = image_map.get(animal, "images/default.jpg")
    hints_html += f"""
    <div class="hint-item">
        <img src="{img}" alt="{animal}">
        <p>{animal}</p>
    </div>
"""

hints_html += """
</div>

<a href="challenge.html" class="back-link">← Back to Challenge</a>

</body>
</html>
"""

with open(f"{OUT_DIR}/hints.html", "w") as f:
    f.write(hints_html)


results_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Results</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<a class="back-main" href="../../game.html">← Main Menu</a>

<h1>Correct Order</h1>
<p>The correct order by <strong>{challenge_type}</strong> (smallest → largest) is:</p>

<div class="results-list">
"""

for i, a in enumerate(correct_order, start=1):
    results_html += f"    <p>{i}. {a}</p>\n"

results_html += """
</div>

<a href="challenge.html" class="restart-link">← Try Again</a>

</body>
</html>
"""

with open(f"{OUT_DIR}/results.html", "w") as f:
    f.write(results_html)

print("Generated HTML pages successfully!")
