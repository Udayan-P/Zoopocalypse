# JSON Specification for "Guess the Animal From Pic" Challenge

## Description
This challenge presents the user with an image of an animal and asks them to guess which animal it is. The challenge includes multiple-choice options, hints, and metadata required to render the puzzle.Further possible modifications of this challenge include reducing photo resolution to increase difficulty 

## JSON Structure

Each challenge is represented by a JSON object with the following fields:

- **challenge_id** (string): Unique ID for the challenge.
- **image** (string): File path to the animal image.
- **question** (string): The question to present to the user.
- **options** (array of strings): List of multiple-choice answers.
- **answer** (string): Correct answer.
- **hints** (array of strings): Hints to be revealed gradually.

## Example JSON

```json
{
  "challenge_id": "animal_001",
  "image": "images/tiger_01.jpg",
  "question": "Which animal is shown in this picture?",
  "options": ["Tiger", "Lion", "Leopard", "Cheetah"],
  "answer": "Tiger",
  "hints": [
    "This animal has stripes.",
    "It is the largest species of cat.",
    "It is native to Asia."
  ]
}
# JSON Specification for “Guess the Animal From Pic” Challenge

## 1. Challenge overview

This challenge shows the player a **blurred image of an animal**.  
The player must correctly identify the animal before their **points reach zero**.

- The image starts heavily blurred.
- The player can:
  - **Reveal textual hints**.
  - **Reveal more of the image** (reduce blur).
- Each help action **costs 1 point**.
- A correct guess:
  - Stops the challenge.
  - Reveals the image clearly.
- If the player runs out of points, the challenge ends and a new animal can be loaded.

The JSON specification below describes everything needed to generate and render a single instance of this challenge.

---

## 2. JSON structure

Each challenge is represented by one JSON object with the following core fields:

- **challenge_id** (`string`):  
  Unique identifier for the challenge, e.g. `"animal_005"`.  
  This is used for logging, debugging and reproducibility.

- **image** (`string`):  
  Relative file path to the animal image used in this challenge,  
  e.g. `"Dataset/Images/Oryx.jpg"`.

- **question** (`string`):  
  The question shown above the options, usually:  
  `"Which animal is shown in this picture?"`  
  (This can be changed to support other phrasings or follow‑up questions.)

- **options** (`array<string>`):  
  List of multiple‑choice answers shown as buttons.  
  The correct answer **must appear exactly once** in this list.  
  The remaining entries are distractor animals, chosen to be plausible.

- **answer** (`string`):  
  The correct answer.  
  Must match one of the entries in `options` exactly.

- **hints** (`array<string>`):  
  Ordered list of textual hints.  
  Hints are revealed one at a time; each reveal:
  - Costs 1 point.
  - Reduces the blur on the image.
  The hints should become progressively more specific.

---

## 3. Optional metadata (for richer hints / analysis)

The challenge JSON can also include additional metadata about the animal.  
These fields are **not required** by the renderer, but are useful for flexible hint generation:

- **diet** (`string`): e.g. `"Herbivore"`, `"Carnivore"`, `"Omnivore"`.
- **habitat** (`string`): e.g. `"Grasslands, Savannas"`, `"Arctic Ocean"`.
- **predators** (`string`): short description of main predators.
- **family** (`string`): biological family, e.g. `"Felidae"`, `"Ursidae"`.
- **conservation_status** (`string`): e.g. `"Least Concern"`, `"Vulnerable"`, `"Endangered"`.

These fields allow the generator to vary hints automatically, for example:

- Hint about **diet** (“This animal is primarily a carnivore.”)
- Hint about **habitat** (“It typically lives in coastal waters.”)
- Hint about **predators** or **family** for late‑stage, more specific clues.

---

## 4. Example JSON object

```json
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
```

This single JSON object contains all the information needed to:

1. Display the blurred image.
2. Show the question and multiple‑choice answers.
3. Reveal progressively more helpful hints.
4. Check whether the player’s selected option is correct.

---

## 5. Flexibility and variation

This specification is deliberately **flexible** and **non‑repetitive**:

- New challenges can be created simply by changing:
  - The `image` path,
  - The `options` and `answer`,
  - And the `hints` list.
- Difficulty can be tuned by:
  - Adjusting how informative each hint is,
  - Changing the number of hints,
  - Choosing more or less confusable distractor animals in `options`.
- Additional metadata fields (diet, habitat, predators, family, conservation status) make it easy to generate varied, meaningful hints automatically from the dataset rather than repeating the same pattern.

This JSON specification therefore supports a wide range of animal images, hint styles and difficulty levels, while still providing a clear structure with **instructions**, **questions**, **hints** and **answers**.