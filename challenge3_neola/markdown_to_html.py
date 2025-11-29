#!/usr/bin/env python3

import sys
import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Feature Challenge</title>
</head>
<body>
{content}
</body>
</html>
"""

def convert_markdown_to_html(md_content):
    return markdown.markdown(md_content)

def main():
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_html.py <input.md> [output.html]")
        sys.exit(1)

    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else md_path.replace(".md", ".html")

    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()

    html_body = convert_markdown_to_html(md)
    rendered = HTML_TEMPLATE.format(content=html_body)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print("Generated HTML:", out_path)

if __name__ == "__main__":
    main()
