#!/usr/bin/env python3

import subprocess
import sys
import glob
from pathlib import Path

PYTHON = "python3"

OUTPUT_JSON = "challenge3_neola/feature_challenge.json"
PAGES_DIR = "challenge3_neola/pages"

def run(cmd):
    print(f"\nRunning: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)
    print("Completed.")

def main():
    # Ensure pages folder exists
    Path(PAGES_DIR).mkdir(exist_ok=True)

    # Step 1 - Generate JSON
    run(f"{PYTHON} challenge3_neola/feature_challenge_generator.py "
        f"challenge3_neola/animals.json {OUTPUT_JSON}")

    # Step 2 - Render markdown into pages/
    run(f"{PYTHON} challenge3_neola/feature_challenge_renderer.py "
        f"{OUTPUT_JSON} --multi --outdir {PAGES_DIR}")

    # Step 3 - Convert all markdown inside pages/ to HTML
    md_files = glob.glob(f"{PAGES_DIR}/*.md")

    if not md_files:
        print("No markdown (.md) files found in pages/. Skipping HTML generation.")
        return

    for f in md_files:
        print(f"\nConverting {f} to HTML")
        run(f"{PYTHON} challenge3_neola/markdown_to_html.py \"{f}\"")

    print("\nPipeline completed successfully. All files are in challenge3_neola/pages/.")

if __name__ == "__main__":
    main()
