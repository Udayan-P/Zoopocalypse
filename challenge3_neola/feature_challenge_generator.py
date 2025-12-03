#!/usr/bin/env python3

import json
import random
import sys
from typing import Dict, List, Any

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print(" No GEMINI_API_KEY found. AI hints will use fallback mode.\n")

GEMINI_MODEL = "models/gemini-2.5-flash"


def generate_ai_hint(animal_name: str, visible_attributes: List[Dict]) -> str:
    """Generate a short Gemini-based simple+smart clue."""

    desc = " | ".join(f"{a['label']}: {a['value']}" for a in visible_attributes)

    if not API_KEY:
        return desc

    prompt = (
        "Generate a SHORT, smart, simple clue (8–12 words) that helps the player "
        "guess an animal WITHOUT revealing its name.\n\n"
        "Tone: clear, concise, slightly clever, not poetic, not scientific.\n"
        "The clue must sound like a real puzzle hint.\n\n"
        f"Use ONLY these attributes: {desc}.\n"
        "Do NOT mention the animal name.\n"
        "Do NOT reveal the species directly."
    )

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        text = (response.text or "").strip()

        if not text:
            raise ValueError("Empty response from Gemini")

        return text

    except Exception as e:
        print(" Gemini hint generation failed, using fallback:", e)
        return desc

def load_dataset(filepath: str) -> List[Dict]:
    try:
        df = pd.read_json(filepath)

        df["AttributeCount"] = df.apply(
            lambda row: sum([1 for v in list(row.values) if v not in [None, "", 0]]),
            axis=1
        )

        df["RarityScore"] = 1 / df["AttributeCount"]

        plot_dir = Path("challenge3_neola/plots")
        plot_dir.mkdir(parents=True, exist_ok=True)

        sns.set(style="whitegrid")
        plt.figure(figsize=(6, 4))
        sns.histplot(df["AttributeCount"], bins=10, kde=True)
        plt.title("Distribution of Attribute Counts in Dataset")
        plot_path = plot_dir / "attribute_count_distribution.png"
        plt.savefig(plot_path)
        plt.close()

        print(f"Loaded dataset with {len(df)} animals")
        print(f"Generated plot: {plot_path}")

        return df.to_dict(orient="records")

    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")

def build_attributes(animal: Dict) -> List[Dict]:
    attributes = []

    fields = {
        "Color": "Color",
        "Height (cm)": "Height",
        "Weight (kg)": "Weight",
        "Lifespan (years)": "Lifespan",
    }
    for src, label in fields.items():
        if src in animal and animal[src]:
            attributes.append({"category": "Descriptive Profile", "label": label, "value": str(animal[src])})

    fields = {
        "Countries Found": "Countries Found",
        "Conservation Status": "Conservation Status",
        "Habitat": "Habitat",
    }
    for src, label in fields.items():
        if src in animal and animal[src]:
            attributes.append({"category": "Geographic & Conservation", "label": label, "value": str(animal[src])})

    if animal.get("Diet"):
        attributes.append({"category": "Diet", "label": "Diet Type", "value": str(animal["Diet"])})

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
            attributes.append({"category": "Physical Features", "label": label, "value": "Yes"})

    traits = {
        "backbone": "Has Backbone",
        "breathes": "Breathes Air",
        "venomous": "Venomous",
        "eggs": "Lays Eggs",
    }
    for field, label in traits.items():
        if animal.get(field) == 1:
            attributes.append({"category": "Biological Traits", "label": label, "value": "Yes"})

    if animal.get("hair") == 1 or animal.get("milk") == 1:
        attributes.append({"category": "Biological Traits", "label": "Warm-Blooded", "value": "Yes"})

    env_fields = {
        "aquatic": "Aquatic",
        "airborne": "Airborne",
        "predator": "Is a Predator",
    }
    for field, label in env_fields.items():
        if animal.get(field) == 1:
            attributes.append({"category": "Habitat & Environment", "label": label, "value": "Yes"})

    if animal.get("Social Structure"):
        attributes.append({"category": "Habitat & Environment", "label": "Social Structure", "value": str(animal["Social Structure"])})

    return attributes

def select_initial_hints(attributes: List[Dict]) -> List[int]:
    idxs = list(range(len(attributes)))
    random.shuffle(idxs)
    return sorted(idxs[:5])

def generate_challenge(dataset: List[Dict], animal_name=None) -> Dict[str, Any]:
    animal = next((a for a in dataset if a.get("Animal") == animal_name), random.choice(dataset))

    print(f"Generating challenge for: {animal.get('Animal')}")

    attributes = build_attributes(animal)
    initial = select_initial_hints(attributes)

    visible_attrs = [attributes[i] for i in initial]

    ai_hint_text = generate_ai_hint(animal.get("Animal"), visible_attrs)

    challenge = {
        "challenge_type": "feature_challenge",
        "animal": animal.get("Animal"),
        "attributes": attributes,
        "initial_hints": initial,
        "max_additional_hints": 5,
        "rarity_score": animal.get("RarityScore"),
        "attribute_count": animal.get("AttributeCount"),
        "dataset_plot": "plots/attribute_count_distribution.png",
        "ai_hint_seed": ai_hint_text,
    }

    return challenge

def main():
    if len(sys.argv) < 3:
        print("Usage: python feature_challenge_generator.py animals.json output.json")
        return

    dataset = load_dataset(sys.argv[1])
    challenge = generate_challenge(dataset)

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(challenge, f, indent=2)

    print("\n✓ Challenge saved:", sys.argv[2])
    print("Initial hints:", challenge["initial_hints"])
    print("AI Hint:", challenge["ai_hint_seed"])


if __name__ == "__main__":
    main()
