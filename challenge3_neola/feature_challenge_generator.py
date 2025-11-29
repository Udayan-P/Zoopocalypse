#!/usr/bin/env python3
"""
Feature Challenge Generator (Synced with Renderer)
Generates challenge JSON files with:
- 5 initial hints
- 5 additional hints
- attribute ordering compatible with renderer
"""

import json
import random
import sys
from typing import Dict, List, Any


def load_dataset(filepath: str) -> List[Dict]:
    """Load animal dataset from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded dataset with {len(data)} animals")
        return data
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")


def build_attributes(animal: Dict) -> List[Dict]:
    """Convert dataset entry → unified attribute list for challenge"""
    attributes = []

    # -------------------------
    # DESCRIPTIVE PROFILE
    # -------------------------
    fields = {
        "Color": "Color",
        "Height (cm)": "Height",
        "Weight (kg)": "Weight",
        "Lifespan (years)": "Lifespan",
    }

    for src, label in fields.items():
        if src in animal and animal[src]:
            attributes.append({
                "category": "Descriptive Profile",
                "label": label,
                "value": str(animal[src])
            })

    # -------------------------
    # GEOGRAPHIC & CONSERVATION
    # -------------------------
    fields = {
        "Countries Found": "Countries Found",
        "Conservation Status": "Conservation Status",
        "Habitat": "Habitat",
    }

    for src, label in fields.items():
        if src in animal and animal[src]:
            attributes.append({
                "category": "Geographic & Conservation",
                "label": label,
                "value": str(animal[src])
            })

    # -------------------------
    # DIET
    # -------------------------
    if animal.get("Diet"):
        attributes.append({
            "category": "Diet",
            "label": "Diet Type",
            "value": str(animal["Diet"])
        })

    # -------------------------
    # PHYSICAL FEATURES (Binary)
    # -------------------------
    binary_features = {
        "hair": "Has Hair",
        "feathers": "Has Feathers",
        "tail": "Has Tail",
        "toothed": "Has Teeth",
        "milk": "Produces Milk",
        "fins": "Has Fins",
    }

    for field, label in binary_features.items():
        if animal.get(field) == 1:
            attributes.append({
                "category": "Physical Features",
                "label": label,
                "value": "Yes"
            })

    # -------------------------
    # BIOLOGICAL TRAITS
    # -------------------------
    traits = {
        "backbone": "Has Backbone",
        "breathes": "Breathes Air",
        "venomous": "Venomous",
        "eggs": "Lays Eggs"
    }

    for field, label in traits.items():
        if animal.get(field) == 1:
            attributes.append({
                "category": "Biological Traits",
                "label": label,
                "value": "Yes"
            })

    # Warm-blooded inference
    if animal.get("hair") == 1 or animal.get("milk") == 1:
        attributes.append({
            "category": "Biological Traits",
            "label": "Warm-Blooded",
            "value": "Yes"
        })

    # -------------------------
    # HABITAT & ENVIRONMENT
    # -------------------------
    env_fields = {
        "aquatic": "Aquatic",
        "airborne": "Airborne",
        "predator": "Is a Predator"
    }

    for field, label in env_fields.items():
        if animal.get(field) == 1:
            attributes.append({
                "category": "Habitat & Environment",
                "label": label,
                "value": "Yes"
            })

    if animal.get("Social Structure"):
        attributes.append({
            "category": "Habitat & Environment",
            "label": "Social Structure",
            "value": str(animal["Social Structure"])
        })

    return attributes


def select_initial_hints(attributes: List[Dict]) -> List[int]:
    """Select exactly 5 initial hints (as renderer expects)"""
    n = len(attributes)
    idxs = list(range(n))
    random.shuffle(idxs)
    return sorted(idxs[:5])  # FIXED: always pick 5


def generate_challenge(dataset: List[Dict], animal_name=None) -> Dict[str, Any]:
    """Generate final challenge JSON (synced with renderer logic)"""
    # Pick animal
    animal = (
        next(a for a in dataset if a.get("Animal") == animal_name)
        if animal_name
        else random.choice(dataset)
    )

    print(f"Generating challenge for: {animal.get('Animal')}")

    attributes = build_attributes(animal)

    if len(attributes) < 5:
        raise RuntimeError("Not enough attributes to select 5 initial hints.")

    initial = select_initial_hints(attributes)

    challenge = {
        "challenge_type": "feature_challenge",
        "animal": animal.get("Animal"),
        "attributes": attributes,
        "initial_hints": initial,
        "max_additional_hints": 5
    }

    return challenge


def main():
    if len(sys.argv) < 2:
        print("Usage: python feature_challenge_generator.py animals.json output.json")
        return

    dataset_path = sys.argv[1]
    output_path = sys.argv[2]

    dataset = load_dataset(dataset_path)
    challenge = generate_challenge(dataset)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(challenge, f, indent=2)

    print("\n✓ Challenge saved:", output_path)
    print("Initial hints:", challenge["initial_hints"])


if __name__ == "__main__":
    main()
