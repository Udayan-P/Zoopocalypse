import random
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from datasets.dataset_loader import load_animals

# Columns from the zoo dataset that make good yes or no style hints
BOOL_HINT_COLS = [
    "hair",
    "feathers",
    "eggs",
    "milk",
    "airborne",
    "aquatic",
    "predator",
    "venomous",
    "fins",
    "tail",
    "domestic",
    "catsize",
]

# Numeric style hints
NUM_HINT_COLS = ["legs"]

# Nicely formatted labels for the hints
HINT_LABELS = {
    "hair": "Has hair",
    "feathers": "Has feathers",
    "eggs": "Lays eggs",
    "milk": "Produces milk",
    "airborne": "Can fly",
    "aquatic": "Aquatic",
    "predator": "Predator",
    "venomous": "Venomous",
    "fins": "Has fins",
    "tail": "Has a tail",
    "domestic": "Domestic animal",
    "catsize": "Big cat sized",
    "legs": "Number of legs",
}

MAX_HINTS = 4  # how many hints we normally use in the game


def _bool_from_str(value: Any) -> Optional[bool]:
    """
    Convert common encodings into a boolean.
    Returns None if the value is not clearly true or false.
    """
    if value is None:
        return None
    v = str(value).strip().lower()
    if v in {"1", "true", "yes", "y"}:
        return True
    if v in {"0", "false", "no", "n"}:
        return False
    return None


def _collect_hints(row: Dict[str, Any]) -> List[Tuple[str, str]]:
    """
    Build a list of (label, value) hint pairs from a single dataset row.
    """
    hints: List[Tuple[str, str]] = []

    # Boolean style hints
    for col in BOOL_HINT_COLS:
        if col not in row:
            continue
        raw = row[col]
        b = _bool_from_str(raw)
        if b is None:
            continue
        label = HINT_LABELS.get(col, col.replace("_", " ").title())
        value = "Yes" if b else "No"
        hints.append((label, value))

    # Numeric hints such as legs
    for col in NUM_HINT_COLS:
        if col not in row:
            continue
        raw = str(row[col]).strip()
        if raw == "":
            continue
        label = HINT_LABELS.get(col, col.replace("_", " ").title())
        value = raw
        hints.append((label, value))

    return hints


def get_random_animal(return_index: bool = False):
    """
    Pick a random animal from the dataset.

    If return_index is False:
        returns (word, hints_dict)

    If return_index is True:
        returns (word, hints_dict, row_index)
    """
    animals = load_animals()
    if not animals:
        raise ValueError("No animals loaded from dataset.")

    idx = random.randrange(len(animals))
    chosen = animals[idx]

    name = chosen.get("animal_name", "").strip().lower()
    if not name:
        # fallback so the game does not completely die
        name = "unknown"

    all_hints = _collect_hints(chosen)
    random.shuffle(all_hints)

    selected = all_hints[:MAX_HINTS]
    if not selected:
        selected = [("General", "This animal is known in the zoo.")]

    hints_dict: Dict[str, str] = {label: value for (label, value) in selected}

    if return_index:
        return name, hints_dict, idx
    return name, hints_dict


def export_hangman_json(word: str, hints: Dict[str, str], row_index: int, out_path: str) -> str:
    """
    Export a hangman challenge in the JSON structure defined in hangman_json_spec.md.
    """
    challenge = {
        "challenge_id": "hangman-auto-{}".format(word),
        "challenge_type": "hangman",
        "word": word.lower(),
        "max_lives": 5,
        "hints": [],
        "dataset_metadata": {
            "dataset_name": "Zoo Animals Dataset",
            "row_index": row_index,
        },
    }

    for label, value in hints.items():
        text = str(value)
        challenge["hints"].append(
            {
                "label": label,
                "text": text,
                "source_column": label,
            }
        )

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(challenge, f, indent=4)

    return str(out_file)


def generate_json_challenge(out_path: str = "json_examples/generated_hangman.json") -> str:
    """
    Create a new hangman challenge from the dataset and write it to a JSON file.
    Returns the path to the generated file.
    """
    word, hints, row_index = get_random_animal(return_index=True)
    return export_hangman_json(word, hints, row_index, out_path)


if __name__ == "__main__":
    # Simple manual test when running this file directly
    out = generate_json_challenge()
    print("Generated Hangman JSON challenge at:", out)