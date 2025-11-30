import json
import random
from pathlib import Path

import pandas as pd

DATASET_DIR = Path("Dataset")     
CSV_PATH = DATASET_DIR / "Zoo Animals Dataset.csv"


def load_dataset() -> pd.DataFrame:
    """
    Load the zoo animals CSV and keep only the columns we care about.
    """
    df = pd.read_csv(CSV_PATH)

    # We only need the label and the image path
    df = df[["animal_name", "Image 1 Path"]].rename(
        columns={
            "animal_name": "label",
            "Image 1 Path": "image_rel_path",
        }
    )
    return df


def make_single_challenge(df: pd.DataFrame) -> dict:
    """
    Pick ONE random animal from the dataset and build a single challenge dict.
    (For now using only placeholder hints.)
    """
    row = df.sample(1).iloc[0]

    label = row["label"]                     # e.g. "elephant"
    image_rel = row["image_rel_path"]        # e.g. "Images/African Elephant.jpg"

    # might build full path later (optional!! but useful for checking files exist)
    image_path = str(DATASET_DIR / image_rel)

    # For now, i use just 2 fake distractors can mprove this later
    all_labels = df["label"].unique().tolist()
    all_labels = [l for l in all_labels if l != label]
    distractors = random.sample(all_labels, 3)

    options = [label] + distractors
    random.shuffle(options)

    challenge = {
        "challenge_id": "animal_001",
        "image": image_rel,  # keeping it relative for the escape room
        "question": "Which animal is shown in this picture?",
        "options": options,
        "answer": label,
        "hints": [
            f"The animal's name starts with '{label[0].upper()}'.",
            "Think about common zoo animals.",
            "Look carefully at the shape and size of the animal.",
        ],
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