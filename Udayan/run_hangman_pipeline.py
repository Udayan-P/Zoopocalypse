##!/usr/bin/env python3
#"""
#Run the full Hangman challenge pipeline.
#
#Steps:
#1. Run generators/hangman_generator.py to create a JSON challenge
#2. Run renderers/hangman_json_renderer.py to render markdown
#3. Run renderers/hangman_markdown_to_html.py to create HTML files
#"""
#
#import subprocess
#import sys
#from pathlib import Path
#
#
#def run(cmd):
#    """Small helper to run a command and show it."""
#    print(f"$ {' '.join(cmd)}")
#    subprocess.run(cmd, check=True)
#
#
#def main() -> None:
#    # Make sure we are in the project root
#    project_root = Path(__file__).resolve().parent
#    print(f"[info] Running pipeline from: {project_root}")
#    print()
#
#    # 1) JSON generation
#    print("[1] Generating Hangman JSON challenge from dataset...")
#    run([sys.executable, "-m", "generators.hangman_generator"])
#    print()
#
#    # 2) JSON -> markdown
#    print("[2] Rendering markdown from JSON files...")
#    run([sys.executable, "-m", "renderers.hangman_json_renderer"])
#    print()
#
#    # 3) markdown -> HTML
#    print("[3] Converting markdown to HTML...")
#    run([sys.executable, "-m", "renderers.hangman_markdown_to_html"])
#    print()
#
#    print("Hangman pipeline finished. Check the json_examples/ and output/ folders.")
#
#
#if __name__ == "__main__":
#    main()

import subprocess
import webbrowser
import sys
import os
import time

SCRIPTS = [
    r"Udayan/generators/hangman_generator.py",
    r"udayan/renderers/hangman_json_renderer.py",
    r"Udayan/renderers/hangman_markdown_to_html.py",
]



def run_script(path):
    print(f"\n▶ Running: {path}")
    result = subprocess.run([sys.executable, path])

    if result.returncode != 0:
        print(f"ERROR: Script failed -> {path}")
        sys.exit(1)

    print(f"Completed: {path}")


def main():

    for script in SCRIPTS:
        run_script(script)
        time.sleep(1)


if __name__ == "__main__":
    main()
