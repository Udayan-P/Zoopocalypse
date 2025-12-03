--------------------
Challenge 1
--------------------

# Guess the Animal – animal_001

JSON Specification — “Guess the Animal From Pic” Challenge

Overview

This challenge shows the player a blurred image of an animal.
Players must identify the correct animal before their points reach zero.
	•	Image begins heavily blurred
	•	Players may:
	•	Reveal hints
	•	Reveal more of the image
	•	Each reveal costs 1 point
	•	A correct answer fully reveals the image
	•	Running out of points ends the challenge

⸻

JSON Structure

Each challenge is represented by one JSON object containing:
	•	challenge_id (string) — Unique identifier
	•	image (string) — File path to the image
	•	question (string) — Usually “Which animal is shown in this picture?”
	•	options (array<string>) — Multiple-choice answers (contains the correct one)
	•	answer (string) — Correct answer
	•	hints (array<string>) — Ordered hints, revealed one by one

⸻

Optional Metadata (Used for Better Hint Generation)

The JSON object may include extra data to generate more meaningful hints:
	•	diet — e.g., “Herbivore”, “Carnivore”
	•	habitat — e.g., “Grasslands”, “Arctic Ocean”
	•	predators — e.g., “Orcas, Bears”
	•	family — e.g., “Felidae”, “Phocidae”
	•	conservation_status — e.g., “Vulnerable”, “Least Concern”

These fields allow:
	•	varied hint generation
	•	progression from general → specific hints
	•	consistent structure across challenges

⸻

Example JSON

{
  "challenge_id": "animal_021",
  "image": "Dataset/Images/Seal 2.jpg",
  "question": "Which animal is shown in this picture?",
  "options": ["seal", "tuatara", "buffalo", "penguin"],
  "answer": "seal",
  "hints": [
    "This animal is primarily a carnivore.",
    "It typically lives in Arctic and Atlantic waters.",
    "Its main predators include polar bears and orcas.",
    "It belongs to the Phocidae family."
  ],
  "diet": "Carnivore",
  "habitat": "Arctic, Atlantic Ocean",
  "predators": "Polar bears, orcas",
  "family": "Phocidae",
  "conservation_status": "Least Concern"
}

⸻

Flexibility & Variation

This format supports many different challenge styles:
	•	Changing the image, options, hints, or metadata creates a new puzzle
	•	Difficulty can be adjusted by:
	•	number of hints
	•	specificity of hints
	•	similarity of distractor animals
	•	Metadata-driven hints ensure non-repetitive, biologically meaningful hint sets

The structure ensures all challenges include:
→ Image, question, options, answer, hints, and (optionally) supporting metadata.
 ![Animal image](Dataset/Images/Bear.jpg)

**Question:** Which animal is shown in this picture?

### Options

- vulture
- gorilla
- bear
- seal

---
### Hints 

- Hint 1: The animal is a carniovre
- Hint 2: Think about common zoo animals.
- Hint 3: Look carefully at the shape and size of the animal.
- Hint 4: It typically lives in Grasslands

---
### Unblurring Effect 
- Image starts off blurry, with each unblur button click, user loses one point.

### Answer (example)

- **Correct answer:** bear
⸻


--------------------
Challenge 3
--------------------

Feature Challenge – JSON Format Specification (Challenge 3)

1. Overview

The Feature Challenge is an animal-identification puzzle represented using a structured JSON file. Each challenge describes one animal using categorized attributes. When players begin:

* Three attributes are revealed initially.
* Players can unlock up to five additional hints during the course of the challenge.
* The rest remain censored unless revealed.
* The answer check is lenient (ex “Tiger” is accepted for “African Tiger”).

This document defines the JSON structure used to represent all Feature Challenge tasks.

2. JSON Structure

A valid challenge must follow:

```json
{
  "challenge_type": "feature_challenge",
  "animal": "string",
  "attributes": [
    { "category": "string", "label": "string", "value": "string" }
  ],
  "initial_hints": [0, 1, 2],
  "max_additional_hints": 5
}
```
3. Attribute Format

Each attribute follows:

```json
{
  "category": "string",
  "label": "string",
  "value": "string"
}
```
Attribute values can be as follows:

* Values may come from text fields (e.g., “Australia”)
* Or from binary dataset fields where 1 → `"Yes"` (e.g., hair = 1 → “Has Hair: Yes”)
* Multiple binary attributes may appear if several fields = 1

4. Attribute Categories

Below are the six categories used in this project. 

4.1 Descriptive Profile

Type: Textual descriptors 
Data Source: Direct text fields from dataset such as:

* Color
* Height (cm)
* Weight (kg)
* Lifespan (years)

These appear as full text (e.g., `"Brown"`, `"120 kg"`, `"15–20 years"`) 

4.2 Geographic & Conservation

Type: Textual descriptors 

Includes:

* Countries Found
* Conservation Status
* Habitat

Values are full descriptive terms from the dataset, ex:

* “Australia”
* “Least Concern”
* “Antarctic Coastal Regions”

4.3 Diet

Type: Fixed classification words (Textual)
Data Source: Direct text fields from dataset such as:

* “Herbivore”
* “Carnivore”
* “Omnivore”
* or combinations (e.g., “Carnivore, Insectivore”)

4.4 Physical Features

Type: Binary dataset fields (0/1) → converted to “Yes” attributes
The dataset provides a number of 0/1 fields such as:

For ex: if dataset field hair = 1, converts to Has Hair: Yes 

You include only the attributes where the dataset value is 1.
Certain times some animals can have 3 or 4 Physical Features showing as “Yes”.

4.5 Biological Traits

Type: Binary dataset fields (0/1) with two special derived traits

Binary fields converted to attributes:

* backbone = 1 → Has Backbone
* breathes = 1 → Breathes Air
* eggs = 1 → Lays Eggs
* venomous = 1 → Venomous

Derived biological traits:

* Warm-Blooded: if `hair = 1` or `milk = 1`
* Cold-Blooded: if `milk = 0` and `feathers = 0`

Again, only includes attributes that evaluate to “Yes”.

4.6 Habitat & Environment

Type: Mixed category
Contains both textual descriptors and binary fields.

Text fields: Habitat description (e.g., “Savannas”, “Eastern Australia”)

Binary fields converted to “Yes”:

* aquatic = 1 → Aquatic
* airborne = 1 → Airborne
* fins = 1 → Marine

Some animals may have multiple environmental flags.

5. Initial Hints

* Always exactly 3 unique indices at the beginning, when the challenge begins.
* These do not count toward the 5 extra hints the player can unlock.

```json
"initial_hints": [0, 3, 8]
```

Hints should ideally come from different categories to avoid making the answer too obvious.

6. Additional Hints

```json
"max_additional_hints": 5
```

* The system allows up to five extra hint reveals.
* These are separate from the initial 3.
* It will be treated as user-requested reveals.

7. Answer Rules

To avoid penalising players for not memorising full regional names:

* Matching is case-insensitive
* Splits animal names into key words
* If the player correctly enters the core animal type, the answer is accepted

Examples:

* Dataset: “African Tiger” → Player answer “Tiger” → Accepted
* Dataset: “Western Gorilla” → Player answer “Gorilla” → Accepted

This makes the gameplay fair and accessible.




--------------------
Challenge 4
--------------------

# Animal Sorting Challenge

Sort the animals **by their Lifespan (years)**, from **smallest → largest**.

## Animals

- **Spectacled Bear**
- **Polar Bear**
- **Atlantic Spotted Dolphin**
- **Yellow-Eyed Penguin**
- **Aardvark**

## Correct Order

Spectacled Bear → Yellow-Eyed Penguin → Atlantic Spotted Dolphin → Aardvark → Polar Bear


