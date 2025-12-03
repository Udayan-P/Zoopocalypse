#!/usr/bin/env python3

import subprocess
import sys
import glob
from pathlib import Path
import os

PYTHON = "python3"

OUTPUT_JSON = "challenge3_neola/feature_challenge.json"
PAGES_DIR = "challenge3_neola/pages"


def run_quiet(cmd):
    """Run a command silently unless an error occurs."""
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")
        sys.exit(1)


def main():

    print("\n Challenge 3 Pipeline Started \n")

    Path(PAGES_DIR).mkdir(exist_ok=True)

    print("• Generating challenge...")
    run_quiet(
        f"{PYTHON} challenge3_neola/feature_challenge_generator.py "
        f"challenge3_neola/animals.json {OUTPUT_JSON}"
    )

    print("• Rendering pages...")
    run_quiet(
        f"{PYTHON} challenge3_neola/feature_challenge_renderer.py "
        f"{OUTPUT_JSON} --multi --outdir {PAGES_DIR}"
    )

    print("• Converting to HTML...")
    md_files = glob.glob(os.path.join(PAGES_DIR, '**', '*.md'), recursive=True)
    for f in md_files:
        run_quiet(f"{PYTHON} challenge3_neola/markdown_to_html.py \"{f}\"")

    print("\n Challenge 3 Pipeline Complete \n")


if __name__ == "__main__":
    main()
