#!/usr/bin/env python3
"""Safely split core-concepts.html into 7 modular section pages, a master

bibliography page, and rebuild core-concepts.html as the primary landing index
portal, preserving every line of data.
"""

from pathlib import Path
import re
import subprocess
import sys


def split_and_generate_modules() -> None:
    root_directory = Path(__file__).resolve().parent
    source_file = root_directory / "core-concepts.html"

    if not source_file.exists():
        print(f"Error: Could not find {source_file}", file=sys.stderr)
        sys.exit(1)

    html_content = source_file.read_text(encoding="utf-8")

    # 1. Extract the <head> block safely
    head_match = re.search(r"(<head>.*?</head>)", html_content, re.DOTALL)
    head_html = head_match.group(1) if head_match else "<head><title>Exam Revision Guide</title></head>"

    # 2. Extract Intro Card & Table of Contents Card for the landing index portal
    intro_card_match = re.search(r'(<div class="intro-card">.*?</div>)', html_content, re.DOTALL)
    toc_card_match = re.search(r'(<nav class="toc-card".*?</nav>)', html_content, re.DOTALL)

    intro_html = intro_card_match.group(1) if intro_card_match else ""
    toc_html = toc_card_match.group(1) if toc_card_match else ""

    # Rewrite TOC links in core-concepts.html to point to the module files
    index_toc_html = toc_html
    for i in range(1, 8):
        index_toc_html = index_toc_html.replace(f'href="#section-{i}"', f'href="module-{i}.html"')
    index_toc_html = index_toc_html.replace('href="#master-bibliography"', 'href="bibliography.html"')

    index_page_content = f"""<!DOCTYPE html>
<html lang="en">
{head_html}
<body>
    <h1>EDCX246 Exam Revision Guide: Forensic Concept Analysis</h1>
    {intro_html}
    {index_toc_html}
</body>
</html>
"""
    source_file.write_text(index_page_content, encoding="utf-8")
    print("Rebuilt core-concepts.html as the landing index portal.")

    # 3. Extract and write each of the 7 sections into module-X.html files
    for i in range(1, 8):
        # Match from <section id="section-i"> to the closing </section>
        pattern = rf'(<section id="section-{i}"\s*>.*?</section>)'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            section_content = match.group(1)
            module_html = f"""<!DOCTYPE html>
<html lang="en">
{head_html}
<body>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    {section_content}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""
            mod_file = root_directory / f"module-{i}.html"
            mod_file.write_text(module_html, encoding="utf-8")
            print(f"Generated: module-{i}.html")

    # 4. Extract and write the Master Bibliography into bibliography.html
    bib_match = re.search(r'(<section id="master-bibliography".*?</section>)', html_content, re.DOTALL)
    if bib_match:
        bib_content = bib_match.group(1)
        bibliography_html = f"""<!DOCTYPE html>
<html lang="en">
{head_html}
<body>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    {bib_content}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""
        bib_file = root_directory / "bibliography.html"
        bib_file.write_text(bibliography_html, encoding="utf-8")
        print("Generated: bibliography.html")

    # 5. Git sync repository
    sync_repository(root_directory, "Modularize revision guide into 7 pages and index portal")


def sync_repository(repo_path: Path, commit_msg: str) -> None:
    commands = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", commit_msg],
        ["git", "push", "origin", "main"],
    ]

    for cmd in commands:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
        if result.returncode != 0:
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("Working tree clean; nothing new to commit.")
                continue
            print(f"Error executing '{' '.join(cmd)}':\n{result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)
        if result.stdout.strip():
            print(result.stdout.strip())

    print("Git repository sync complete.")


if __name__ == "__main__":
    split_and_generate_modules()
