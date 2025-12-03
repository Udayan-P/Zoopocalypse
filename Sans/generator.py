import json
import random
from pathlib import Path

import pandas as pd

# Folder that contains CSV and Images folder, make sure linked proper

BASE_DIR = Path(__file__).resolve().parent          # Sans/
DATASET_DIR = BASE_DIR / "Dataset"                  # Sans/Dataset
CSV_PATH = DATASET_DIR / "Zoo Animals Dataset.csv"  # Sans/Dataset/Zoo Animals Dataset.csv


def load_dataset() -> pd.DataFrame:
    """
    Load the zoo animals CSV and keep all columns, but rename the ones
    we commonly use in the challenge builder.
    """
    df = pd.read_csv(CSV_PATH)

    # keep all columns, just rename these for convenience
    df = df.rename(
        columns={
            "animal_name": "label",
            "Image 1 Path": "image_rel_path",
        }
    )
    return df


def build_hints(row) -> list:
    """
    Build a small set of biologically meaningful hints from the dataset row.
    Uses real columns like Diet, Habitat, Predators, Family, Conservation Status.
    """
    name = str(row.get("label", "")).strip() or "This animal"
    diet = str(row.get("Diet", "")).strip()
    habitat = str(row.get("Habitat", "")).strip()
    predators = str(row.get("Predators", "")).strip()
    family = str(row.get("Family", "")).strip()
    status = str(row.get("Conservation Status", "")).strip()

    hints = []


    # 2. Diet-based hint
    if diet and diet.lower() not in {"not applicable", "varies"}:
        hints.append(f"This animal is primarily a {diet.lower()}.")

    # 3. Habitat-based hint
    if habitat and habitat.lower() not in {"varies"}:
        hints.append(f"It typically lives in {habitat.lower()}.")

    # 4. Predators
    if predators and predators.lower() not in {"not applicable"}:
        hints.append(f"Its main predators include {predators.lower()}.")

    # 5. Family
    if family and family.lower() not in {"not applicable"}:
        hints.append(f"It belongs to the {family} family.")

    # 6. Conservation status
    if status and status.lower() not in {"not applicable"}:
        hints.append(f"Its conservation status is {status.lower()}.")

    # Don’t overwhelm the player; keep 3–4 hints max
    if len(hints) > 4:
        hints = hints[:4]

    # If somehow we ended up with none (e.g. missing columns), fall back
    if not hints:
        hints = [
            "Look carefully at the overall shape and posture of the animal.",
            "Pay attention to details like the head, limbs, and tail.",
            "Think about whether this animal is more likely to live on land, in water, or in the air.",
        ]

    return hints


def make_single_challenge(df: pd.DataFrame, challenge_id: int = 1) -> dict:
    """
    Pick ONE random animal from the dataset and build a single challenge dict.
    """
    row = df.sample(1).iloc[0]

    label = str(row["label"])              # e.g. "elephant"
    image_rel = str(row["image_rel_path"]) # e.g. "Images/Seal.jpg"

    # This is the path from the project root to the image file,
    # which is what the markdown needs:
    # Dataset/Images/Seal.jpg
    image_for_markdown = str(DATASET_DIR / image_rel)

    #  distractor labels (all labels except the correct one)
    all_labels = df["label"].unique().tolist()
    all_labels = [l for l in all_labels if l != label]

    #  be safe about how many we sample
    num_distractors = min(7, len(all_labels))
    distractors = random.sample(all_labels, num_distractors)

    options = [label] + distractors
    random.shuffle(options)

    hints = build_hints(row)

    challenge = {
        "challenge_id": f"animal_{challenge_id:03d}",
        "image": image_for_markdown,
        "question": "Which animal is shown in this picture?",
        "options": options,
        "answer": label,
        "hints": hints,
    }

    return challenge


def main():
    df = load_dataset()
    challenge = make_single_challenge(df)

    # save to a JSON file
    output_path = Path("generated_challenge.json")
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(challenge, f, indent=4)

    print(f"Saved challenge to {output_path}")


if __name__ == "__main__":
    main()