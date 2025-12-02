import unicodedata
import re
from pathlib import Path

import pandas as pd

DATASET_DIR = Path("Dataset")
CSV_NAME = "Zoo Animals Dataset.csv"
IMAGES_DIR = DATASET_DIR / "Images"


def clean_animal_name(name: str) -> str:
    """
    Turn 'Galápagos Penguin!!!' -> 'Galapagos Penguin'
    - remove accents
    - keep letters, numbers and spaces
    - collapse multiple spaces
    - Title Case the words
    """
    # remove accents
    nfkd = unicodedata.normalize("NFKD", name)
    no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))

    # keep only letters / numbers / spaces
    cleaned = re.sub(r"[^A-Za-z0-9 ]+", "", no_accents)

    # collapse spaces and strip
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Title Case with spaces (no underscores)
    pretty = " ".join(word.capitalize() for word in cleaned.split())
    return pretty


def main():
    csv_path = DATASET_DIR / CSV_NAME
    df = pd.read_csv(csv_path)

    if "animal_name" not in df.columns or "Image 1 Path" not in df.columns:
        raise ValueError("CSV must contain 'animal_name' and 'Image 1 Path' columns.")

    # backup CSV
    backup_path = DATASET_DIR / (CSV_NAME.replace(".csv", "_backup_original.csv"))
    csv_path.rename(backup_path)
    print(f"Backup CSV saved as: {backup_path}")

    # to avoid overwriting if same animal appears twice
    used_names = {}

    new_paths = []

    for idx, row in df.iterrows():
        animal = str(row["animal_name"])
        old_rel = str(row["Image 1 Path"])  # e.g. 'Images/Galápagos Penguin.jpg'
        old_path = DATASET_DIR / old_rel

        if not old_path.exists():
            print(f"WARNING: file not found for row {idx}: {old_path}")
            new_paths.append(old_rel)
            continue

        base_name = clean_animal_name(animal)

        # handle duplicates
        count = used_names.get(base_name, 0) + 1
        used_names[base_name] = count

        if count == 1:
            final_base = base_name
        else:
            # e.g. 'African Lion 2'
            final_base = f"{base_name} {count}"

        suffix = old_path.suffix or ".jpg"  # keep original extension
        new_filename = f"{final_base}{suffix}"
        new_rel = f"Images/{new_filename}"
        new_path = IMAGES_DIR / new_filename

        # rename file
        old_path.rename(new_path)

        print(f"Renamed: {old_rel}  ->  {new_rel}")
        new_paths.append(new_rel)

    # update CSV with new paths
    df["Image 1 Path"] = new_paths
    df.to_csv(csv_path, index=False)
    print(f"Updated CSV written to: {csv_path}")


if __name__ == "__main__":
    main()