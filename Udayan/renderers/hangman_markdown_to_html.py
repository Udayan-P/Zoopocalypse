#!/usr/bin/env python3
"""
Hangman markdown to HTML converter.

Reads the markdown files produced by hangman_json_renderer.py
and writes simple HTML files into the output/ folder.

Usage (from project root):

    python3 -m renderers.hangman_markdown_to_html
"""

from pathlib import Path

try:
    import markdown  # external package, see note in main
except ImportError:
    markdown = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"


def md_to_html(md_text: str, title: str) -> str:
    """Convert markdown text into a basic HTML page."""
    if markdown is None:
        # Very small fallback if the markdown package is not installed.
        # This is not a full markdown renderer, only a basic backup.
        body = (
            md_text.replace("\n\n", "<br><br>\n")
            .replace("\n", "<br>\n")
        )
    else:
        body = markdown.markdown(md_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 800px;
            margin: 2rem auto;
            line-height: 1.5;
            background: #111;
            color: #f5f5f5;
        }}
        h1, h2, h3 {{
            color: #ffd27f;
        }}
        code {{
            background: #222;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        pre {{
            background: #222;
            padding: 0.75rem;
            border-radius: 4px;
            overflow-x: auto;
        }}
        a {{
            color: #7fdcff;
        }}
    </style>
</head>
<body>
{body}
</body>
</html>
"""
    return html


def convert_file(md_name: str, html_name: str) -> None:
    """Load one markdown file from output/ and write the HTML version."""
    md_path = OUTPUT_DIR / md_name
    html_path = OUTPUT_DIR / html_name

    if not md_path.exists():
        print(f"[warn] Markdown file not found: {md_path}")
        return

    text = md_path.read_text(encoding="utf-8")
    html = md_to_html(text, title=html_name.replace(".html", ""))

    html_path.write_text(html, encoding="utf-8")
    print(f"[ok] Wrote {html_path}")


def main() -> None:
    if markdown is None:
        print(
            "[note] python-markdown package not found. "
            "Using very simple fallback conversion.\n"
            "To install the proper renderer: pip install markdown"
        )

    convert_file("hangman_example.md", "hangman_example.html")
    convert_file("hangman_generated.md", "hangman_generated.html")


if __name__ == "__main__":
    main()