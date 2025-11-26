import random
from datasets.dataset_loader import load_animals

def get_random_animal():
    """
    Selects a random animal from the dataset and returns:
    1. the animal name as the hangman word
    2. a hint dictionary created from useful attributes
    """
    animals = load_animals()
    chosen = random.choice(animals)

    # Clean the word for hangman (lowercase, no spaces)
    word = chosen["animal_name"].strip().lower()

    # Build hint set from available attributes
    hints = {}

    # Add hints only if they exist in the dataset
    if "class" in chosen:
        hints["Classification"] = chosen["class"]

    if "diet" in chosen:
        hints["Diet"] = chosen["diet"]

    if "location" in chosen:
        hints["Found in"] = chosen["location"]

    if "type" in chosen:
        hints["Type"] = chosen["type"]

    # Fallback hint if dataset is missing fields
    if not hints:
        hints["General"] = "This animal is known in the zoo."

    return word, hints


if __name__ == "__main__":
    # Debug test
    word, hints = get_random_animal()
    print("Chosen word:", word)
    print("Hints:")
    for key, value in hints.items():
        print(f" - {key}: {value}")