import os

def generate_patterns(randomized_list, correct_order):
    return [correct_order.index(animal) + 1 for animal in randomized_list]

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
        challenge_type = line[start:end].strip().replace("**", "")
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

# ------------------------------
# IMAGE MAP FOR DROPDOWN CARDS
# ------------------------------
image_map = {}
for animal in animals: 
    animal_text = animal.strip().replace(" ", " ").replace("  ", " ")
    #animal_text = animal.replace(" ", "_")
    image_map[animal] = f"generated_animal_images/{animal_text}.jpg"
# ------------------------------
# CHALLENGE PAGE (CSS DROPDOWNS)
# ------------------------------

challenge_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Animal Sorting Challenge</title>
    <link rel="stylesheet" href="style.css">

<style>

.dropdown-card {{
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 12px;
    margin: 12px 0;
    cursor: pointer;
    background: #fafafa;
    transition: 0.2s;
}}

.dropdown-card:hover {{
    background: #f0f0f0;
}}

.dropdown-card label {{
    font-weight: bold;
    cursor: pointer;
    display: block;
}}

.dropdown-checkbox {{
    display: none;
}}

.dropdown-content {{
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;
}}

.dropdown-checkbox:checked + .dropdown-content {{
    max-height: 400px;
}}

.dropdown-content img {{
    width: 250px;
    margin-top: 10px;
    border-radius: 6px;
}}
</style>
</head>
<body>

<a class="back-main" href="../../game.html">← Main Menu</a>

<h1>Animal Sorting Challenge</h1>
<p>Sort the animals by <strong>smallest → largest</strong> {challenge_type}.</p>

<p>(For hints click on the animal names to reveal AI generated image of the animals)</p>

<div class="animal-list">
"""

# PURE HTML+CSS DROPDOWNS (NO JS)
count = 1
for i, animal in enumerate(animals, start=1):

    checkbox_id = f"dropdown_{i}"

    challenge_html += f"""
    <div class="dropdown-card">
        <label for="{checkbox_id}">{i}. {animal}</label>
        <input type="checkbox" id="{checkbox_id}" class="dropdown-checkbox">
        <div class="dropdown-content">
            <img src="../generated_animal_images/{count}.png" alt="{animal}">
        </div>
    </div>
"""
    count += 1

challenge_html += """
</div>

<h3>Your Answer:</h3>

<form action="results.html" method="get">
    <div class="inputs">
"""

for p in pattern:
    challenge_html += f'<input type="text" placeholder="Number Only" pattern="{p}" required>\n'

challenge_html += """
    </div>
    <button type="submit">Check Answer →</button>
</form>

</body>
</html>
"""

with open(f"{OUT_DIR}/challenge.html", "w") as f:
    f.write(challenge_html)

# ------------------------------
# RESULTS PAGE
# ------------------------------

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
