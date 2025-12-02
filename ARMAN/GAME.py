import subprocess
import webbrowser
import sys
import os
import time

SCRIPTS = [
    r"ARMAN/json_generator.py",
    r"ARMAN/order_game_renderer.py",
    r"ARMAN/html_generator.py",
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
