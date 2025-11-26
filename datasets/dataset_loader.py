import csv
from pathlib import Path

DATASET_PATH = Path(__file__).parent / "Zoo_Animals_Dataset.csv"

def load_animals():
    """
    Loads zoo animals dataset and returns a list of dictionaries.
    Each dictionary represents an animal and its attributes.
    """
    animals = []
    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            animals.append(row)
    return animals

if __name__ == "__main__":
    # Debug print to confirm the loader works
    data = load_animals()
    print(f"Loaded {len(data)} animals.")
    print(data[0])  # show the first entry