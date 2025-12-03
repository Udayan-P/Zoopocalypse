import subprocess
import webbrowser
import sys
import os
import time

SCRIPTS = [
    r"ARMAN/GAME.py",
    r"challenge3_neola/feature_challenge_pipeline.py",
    r"Udayan/run_hangman_pipeline.py",
    r"Sans/animal_challenge_pipeline.py",
]

md_files = [
    "challenge1.md",
    "Udayan/output/hangman_generated.md",
    "challenge3.md",
    "ARMAN/challenge1.md"
]

def combine_markdowns(md_files, output_file="combined.md"):

    with open(output_file, "w", encoding="utf-8") as out:
        for i, md_path in enumerate(md_files, start=1):

            if not os.path.exists(md_path):
                print(f"Warning: File not found: {md_path}")
                continue

            out.write("--------------------\n")
            out.write(f"Challenge {i}\n")
            out.write("--------------------\n\n")

            with open(md_path, "r", encoding="utf-8") as f:
                out.write(f.read())
                out.write("\n\n")

    print(f"Combined file created: {output_file}")

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

    time.sleep(1)
    html_path = os.path.abspath("game.html")
    print(f"\nOpening {html_path}")
    webbrowser.open(f"file://{html_path}")

    combine_markdowns(md_files, "all_challenges.md")

    print("\nAll tasks completed successfully!\n")


if __name__ == "__main__":
    main()
