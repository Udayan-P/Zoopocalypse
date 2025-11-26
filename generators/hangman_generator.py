import random
from typing import Dict, Any, List, Tuple, Optional

from datasets.dataset_loader import load_animals

# Columns from the zoo dataset that make good yes/no hints
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

# Special numeric style hint
NUM_HINT_COLS = ["legs"]

# Nice labels for the hint text
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

MAX_HINTS = 4  # how many hints to show in the game


def _bool_from_str(value: str) -> Optional[bool]:
    """
    Convert common string encodings into a boolean.
    Returns None if the value is not obviously true or false.
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
    Build a list of (label, value) hint pairs from a single animal row.
    Uses the zoo dataset columns like hair, feathers, legs and so on.
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

    # Numeric hints like legs
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


def get_random_animal() -> Tuple[str, Dict[str, str]]:
    """
    Selects a random animal from the dataset and returns:
    - the animal name as the hangman word
    - a dictionary of hints built from its attributes
    """
    animals = load_animals()
    chosen = random.choice(animals)

    # animal_name is the column we use as the word
    name = chosen.get("animal_name", "").strip().lower()

    # collect all possible hints
    all_hints = _collect_hints(chosen)

    # shuffle so hints are not always in the same order
    random.shuffle(all_hints)

    # take the first few hints
    selected = all_hints[:MAX_HINTS]

    # if for some reason we did not get any hints, fall back to a generic one
    if not selected:
        selected = [("General", "This animal is known in the zoo.")]

    # convert list of pairs to a dictionary for the renderer
    hints_dict: Dict[str, str] = {label: value for label, value in selected}

    return name, hints_dict


if __name__ == "__main__":
    # Simple debug run to check output looks sensible
    word, hints = get_random_animal()
    print("Chosen word:", word)
    print("Hints:")
    for k, v in hints.items():
        print(f" - {k}: {v}")