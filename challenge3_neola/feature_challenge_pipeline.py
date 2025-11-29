#!/usr/bin/env python3

import subprocess
import sys
import glob

PYTHON = "python3"  # Adjust if needed

OUTPUT_JSON = "feature_challenge.json"

def run(cmd):
    print(f"\nRunning: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)
    print("Completed.")

def main():
    # Step 1: Generate challenge JSON
    run(f"{PYTHON} feature_challenge_generator.py animals.json {OUTPUT_JSON}")

    # Step 2: Render markdown files
    run(f"{PYTHON} feature_challenge_renderer.py {OUTPUT_JSON} --multi")

    # Step 3: Convert all markdown files to HTML
    md_files = glob.glob("*.md")
    if not md_files:
        print("No markdown (.md) files found. Skipping HTML generation.")
        return

    for f in md_files:
        print(f"\nConverting {f} to HTML")
        run(f"/opt/anaconda3/bin/python3 markdown_to_html.py \"{f}\"")

    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main()
