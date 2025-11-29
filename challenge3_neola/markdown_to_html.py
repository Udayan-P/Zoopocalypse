#!/usr/bin/env python3

import sys
import re
from pathlib import Path
import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Feature Challenge</title>
<style>
.category-card {{
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 24px 0;
}}
.button-row {{
    margin-top: 20px;
}}
.button-row a {{
    margin-right: 8px;
}}
</style>
</head>
<body>
{content}
</body>
</html>
"""

def convert_markdown_to_html(md_content):

    html = markdown.markdown(md_content, extensions=["extra"])

    # Wrap categories
    html = re.sub(
        r"(<h3>[^<]+</h3>\s*<ul>[\s\S]*?</ul>)",
        r'<div class="category-card">\1</div>',
        html,
    )

    # Convert <a> | <a> into row
    def convert_buttons(match):
        block = match.group(0)
        links = re.findall(r'<a href="([^"]+)">(.*?)</a>', block)
        new = "<div class='button-row'>" + "".join(
            f"<a href='{href}'>{label}</a>" for href, label in links
        ) + "</div>"
        return new

    html = re.sub(
        r"<p>\s*(?:<a href=\"[^\"]+\">.*?</a>\s*\|\s*)*<a href=\"[^\"]+\">.*?</a>\s*</p>",
        convert_buttons,
        html,
    )

    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_html.py <input.md> [output.html]")
        sys.exit(1)

    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else md_path.replace(".md", ".html")

    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()

    body_html = convert_markdown_to_html(md)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.format(content=body_html))

    print("Generated HTML:", out_path)

if __name__ == "__main__":
    main()
