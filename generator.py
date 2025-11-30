import json
import random
from pathlib import Path

import pandas as pd

# Folder that contains CSV and Images folder, make sure linked proper
DATASET_DIR = Path("Dataset")
CSV_PATH = DATASET_DIR / "Zoo Animals Dataset.csv"


def load_dataset() -> pd.DataFrame:
    """
    Load the zoo animals CSV and keep only the columns we care about.
    """
    df = pd.read_csv(CSV_PATH)

    #only need the label and the image path
    df = df[["animal_name", "Image 1 Path"]].rename(
        columns={
            "animal_name": "label",
            "Image 1 Path": "image_rel_path",
        }
    )
    return df


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
    num_distractors = min(3, len(all_labels))
    distractors = random.sample(all_labels, num_distractors)

    options = [label] + distractors
    random.shuffle(options)

    challenge = {
        "challenge_id": f"animal_{challenge_id:03d}",
        "image": image_for_markdown,  # this will be "Dataset/Images/Seal.jpg"
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