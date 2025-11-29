#!/usr/bin/env python3

import json
import random
import sys

def load_dataset(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print("Error loading dataset")
        sys.exit(1)

def build_attributes(animal):
    attributes = []

    desc = {
        "Color": "Color",
        "Height (cm)": "Height",
        "Weight (kg)": "Weight",
        "Lifespan (years)": "Lifespan"
    }
    geo = {
        "Countries Found": "Countries Found",
        "Conservation Status": "Conservation Status",
        "Habitat": "Habitat"
    }

    for src, label in desc.items():
        if src in animal:
            attributes.append({
                "category": "Descriptive Profile",
                "label": label,
                "value": str(animal[src])
            })

    for src, label in geo.items():
        if src in animal:
            attributes.append({
                "category": "Geographic & Conservation",
                "label": label,
                "value": str(animal[src])
            })

    if animal.get("Diet"):
        attributes.append({
            "category": "Diet",
            "label": "Diet Type",
            "value": animal["Diet"]
        })

    physical_binary = {
        "hair": "Has Hair",
        "feathers": "Has Feathers",
        "tail": "Has Tail",
        "milk": "Produces Milk"
    }
    for field, label in physical_binary.items():
        if animal.get(field) == 1:
            attributes.append({
                "category": "Physical Features",
                "label": label,
                "value": "Yes"
            })

    if animal.get("hair") == 1 or animal.get("milk") == 1:
        attributes.append({
            "category": "Biological Traits",
            "label": "Warm-Blooded",
            "value": "Yes"
        })

    return attributes

def pick_initial_hints(attributes):
    idxs = list(range(len(attributes)))
    random.shuffle(idxs)
    return sorted(idxs[:5])

def generate_challenge(dataset, animal_name=None):
    if animal_name:
        selected = next((a for a in dataset if a["Animal"] == animal_name), None)
        if not selected:
            raise RuntimeError("Animal not found.")
    else:
        selected = random.choice(dataset)

    attributes = build_attributes(selected)
    initial = pick_initial_hints(attributes)

    return {
        "challenge_type": "feature_challenge",
        "animal": selected["Animal"],
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
