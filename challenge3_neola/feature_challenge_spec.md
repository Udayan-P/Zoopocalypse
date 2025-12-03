Feature Challenge – JSON Format Specification (Challenge 3)

1. Overview**

The Feature Challenge is an animal-identification puzzle represented using a structured JSON file. Each challenge describes one animal using categorized attributes. When players begin:

* Five attributes are revealed initially to start the puzzle.
* Players may unlock up to three additional hints during the course of the challenge.
* All remaining attributes stay censored unless revealed.
* Players have 2 wrong attempts to guess the species.
* A single AI-generated clue is included and remains constant for the entire challenge.
* The answer can be picked from the 8 options given to the user.

These settings are chosen specifically to maintain a balanced difficulty level, ensuring the challenge remains solvable but not trivial.

This document defines the JSON structure used to represent all Feature Challenge tasks.

2. JSON Structure**

A valid challenge must follow:

```json
{
  "challenge_type": "feature_challenge",
  "animal": "string",
  "attributes": [
    { "category": "string", "label": "string", "value": "string" }
  ],
  "initial_hints": [0, 1, 2, 3, 4],
  "max_additional_hints": 3,
  "ai_hint_seed": "string"
}
```

Field Notes:

* initial_hints
  Always contains 5 unique indices**, representing the 5 attributes revealed at game start.

* max_additional_hints
  Always 3, controlling how many more hints the user can unlock.

* ai_hint_seed
  A short AI-generated clue derived from the visible attributes.
  It is static and does not change across attempts.

3. Attribute Format

Each attribute follows:

```json
{
  "category": "string",
  "label": "string",
  "value": "string"
}
```

Attribute values may be:

* Text descriptors (e.g., `"Australia"`, `"120 kg"`)
* Derived values from binary dataset fields (`0/1 → "Yes"`)
* Multiple attributes may appear for the same category depending on dataset content

4. Attribute Categories

The system uses the six attribute categories below.

* 4.1 Descriptive Profile

Type: Textual descriptors
Source: Dataset fields such as:

* Color
* Height (cm)
* Weight (kg)
* Lifespan (years)

* 4.2 Geographic & Conservation

Type: Textual descriptors

Examples:

* `"Australia"`
* `"Least Concern"`
* `"Antarctic Coastal Regions"`

*4.3 Diet

Type: Text classification
Source examples: `"Herbivore"`, `"Carnivore"`, `"Omnivore"`

Combined types (e.g., `"Carnivore, Insectivore"`) are also valid.

* 4.4 Physical Features

Type: Binary dataset fields (1 → “Yes”)

Examples:

* `hair = 1` → `"Has Hair"`
* `milk = 1` → `"Produces Milk"`
* `feathers = 1` → `"Has Feathers"`

Only fields where the dataset value is 1 become attributes.

* 4.5 Biological Traits

Type: Binary + derived traits

Binary conversions:

* `backbone = 1` → `"Has Backbone"`
* `breathes = 1` → `"Breathes Air"`
* `eggs = 1` → `"Lays Eggs"`
* `venomous = 1` → `"Venomous"`

Derived traits:

* `"Warm-Blooded"` if `hair = 1` or `milk = 1`
* `"Cold-Blooded"` if `milk = 0` and `feathers = 0`

Only positive traits are included.

* 4.6 Habitat & Environment

Type: Mixed textual + binary fields

Textual:

* Habitat regions (e.g., `"Savannas"`, `"Eastern Australia"`)

Binary conversions:

* `aquatic = 1` → `"Aquatic"`
* `airborne = 1` → `"Airborne"`
* `fins = 1` → `"Marine"`

Animals may have multiple environmental attributes.

* 5. Initial Hints 

Initial hints are:

```json
"initial_hints": [0, 3, 5, 7, 9]
```

Rules:

* Always 5 indices.
* These correspond to five attributes shown at the beginning.
* They do not count toward additional hint unlocks.
* The renderer typically spreads hints across categories to avoid making the answer trivial.

* 6. Additional Hints

```json
"max_additional_hints": 3
```

Rules:

* Only 3 additional attributes can be revealed.
* These are triggered by the player's request (“Reveal Next Hint”).
* 3 to maintain difficulty and ensure the species is not overexposed.

*7. AI Hint 

Each challenge contains:

```json
"ai_hint_seed": "A short AI-generated clue"
```

Properties:

* Generated once and can be viewed at any point of the game.
* Does not update as more hints unlock.
* Should be short (8–12 words), simple, and not reveal the species directly.
* Provides an optional assist while keeping the difficulty reasonable.

* 8. Answer Rules

User has 8 options to pick the answer from with 2 valid attempts before the answer can be revealed.




