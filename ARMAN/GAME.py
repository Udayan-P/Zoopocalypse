import subprocess
import webbrowser
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("🔄 Running JSON generator...")
subprocess.run(["python", "generate_json.py"], check=True)

print("📝 Running Markdown generator...")
subprocess.run(["python", "json_to_markdown.py"], check=True)

print("🌐 Generating HTML pages...")
subprocess.run(["python", "markdown_to_html.py"], check=True)

challenge_path = os.path.abspath("html/challenge.html")
print(f"🚀 Opening {challenge_path}")
webbrowser.open(f"file://{challenge_path}")