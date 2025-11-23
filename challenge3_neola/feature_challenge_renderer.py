#!/usr/bin/env python3
import json
import sys


def load_json(path):
    """Load the challenge JSON and check required fields exist."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: input file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: invalid JSON format.")
        sys.exit(1)

    # Basic required fields for feature challenge
    required = ["challenge_type", "animal", "attributes", "initial_hints", "max_additional_hints"]
    for field in required:
        if field not in data:
            print(f"Error: missing required field '{field}'.")
            sys.exit(1)

    return data


def main():
    """For now, only load and validate the JSON file."""
    if len(sys.argv) < 2:
        print("Usage: python feature_challenge_renderer.py <input.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    data = load_json(input_file)

    print("✓ JSON loaded successfully.")
    print(f"Animal in this challenge: {data['animal']}")
    print("Renderer logic will be added in the next stages.")


if __name__ == "__main__":
    main()
