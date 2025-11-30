import subprocess
import webbrowser
import sys
import os
import time

SCRIPTS = [
    r"ARMAN/GAME.py",
    r"challenge3_neola/feature_challenge_pipeline.py",
    r"Udayan/run_hangman_pipeline.py",
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

    time.sleep(1)
    html_path = os.path.abspath("game.html")
    print(f"\nOpening {html_path}")
    webbrowser.open(f"file://{html_path}")

    print("\nAll tasks completed successfully!\n")


if __name__ == "__main__":
    main()
