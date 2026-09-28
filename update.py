#!/usr/bin/env python3
"""Move the Interactive Forensic Revision Portal banner to be directly under

the table of contents in index.html, matching index.html's blue/slate color scheme.
"""

from pathlib import Path
import re
import subprocess
import sys


def update_index_html(root_dir: Path) -> None:
    index_file = root_dir / "index.html"
    if not index_file.exists():
        print("index.html not found.")
        return

    content = index_file.read_text(encoding="utf-8")

    # 1. Clean up any existing access banners to avoid duplicates or old color schemes
    content = re.sub(
        r'\s*<!-- ACCESS BANNER TO FORENSIC REVISION PORTAL -->.*?(?=<h2|<div class="book-overview-card"|<nav id="table-of-contents"|<h1|$)',
        "",
        content,
        flags=re.DOTALL,
    )

    # 2. Define the new banner matching index.html's blue/slate scheme (#1e40af, #f8fafc, #cbd5e1)
    blue_banner_html = """
    <!-- ACCESS BANNER TO FORENSIC REVISION PORTAL -->
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 6px solid #1e40af; border-radius: 8px; padding: 22px 26px; margin: 32px 0; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div style="flex-grow: 1; min-width: 280px;">
            <h3 style="margin: 0 0 6px 0; color: #1e40af; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.03em;">Interactive Forensic Revision Portal</h3>
            <p style="margin: 0; font-size: 0.94rem; color: #334155; line-height: 1.5; text-align: justify;">Access the complete modular revision guide featuring four-part dossiers, interactive popovers, concrete classroom scenarios, SVG architecture diagrams, and critical rebuttals.</p>
        </div>
        <a href="core-concepts.html" style="display: inline-flex; align-items: center; padding: 10px 18px; background-color: #1e40af; color: #ffffff; border-radius: 6px; text-decoration: none; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.02em; transition: background-color 0.15s ease-in-out; flex-shrink: 0;">Launch Portal &rarr;</a>
    </div>
"""

    # 3. Locate the table of contents block and insert the banner *after* it
    toc_pattern = r'(<nav id="table-of-contents".*?</nav>)'
    match = re.search(toc_pattern, content, re.DOTALL)
    if match:
        toc_end_pos = match.end()
        content = content[:toc_end_pos] + "\n" + blue_banner_html + content[toc_end_pos:]
        index_file.write_text(content, encoding="utf-8")
        print("Successfully moved and restyled the forensic portal banner under the table of contents in index.html[cite: 1].")
    else:
        print("Warning: Table of contents element not found in index.html[cite: 1].", file=sys.stderr)


def execute_git_sync(repo_path: Path, commit_msg: str) -> None:
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


def main() -> None:
    root_directory = Path(__file__).resolve().parent
    update_index_html(root_directory)

    commit_message = (
        "Move forensic portal banner under table of contents in index.html\n\n"
        "Style the portal access banner to match index.html's blue/slate color scheme\n"
        "and place it directly after the Table of Contents navigation card."
    )

    execute_git_sync(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
