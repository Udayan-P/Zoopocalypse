#!/usr/bin/env python3

import json
import random
import sys

def load_dataset(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_attributes(animal):
    attributes = []

    fields = {
        "Color": "Color",
        "Height (cm)": "Height",
        "Weight (kg)": "Weight",
        "Lifespan (years)": "Lifespan",
        "Countries Found": "Countries Found",
        "Conservation Status": "Conservation Status",
        "Habitat": "Habitat"
    }

    for src, label in fields.items():
        if src in animal and animal[src]:
            attributes.append({
                "category": "Descriptive Profile" if "cm" in src or "kg" in src or "Color" in src or "Lifespan" in src else "Geographic & Conservation",
                "label": label,
                "value": str(animal[src])
            })

    if animal.get("Diet"):
        attributes.append({
            "category": "Diet",
            "label": "Diet Type",
            "value": animal["Diet"]
        })

    binary = ["hair", "feathers", "tail", "milk"]
    for field in binary:
        if animal.get(field) == 1:
            attributes.append({
                "category": "Physical Features",
                "label": f"Has {field.capitalize()}",
                "value": "Yes"
            })

    return attributes

def generate_challenge(dataset):
    animal = random.choice(dataset)
    attributes = build_attributes(animal)

    idxs = list(range(len(attributes)))
    random.shuffle(idxs)
    initial = sorted(idxs[:5])

    return {
        "challenge_type": "feature_challenge",
        "animal": animal["Animal"],
        "attributes": attributes,
        "initial_hints": initial,
        "max_additional_hints": 5
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python generator.py animals.json output.json")
        return

    dataset = load_dataset(sys.argv[1])
    challenge = generate_challenge(dataset)

    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(challenge, f, indent=2)

if __name__ == "__main__":
    main()
