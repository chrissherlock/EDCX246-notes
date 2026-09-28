#!/usr/bin/env python3
"""Inject in-page Table of Contents navigation cards into each module page

(module-1.html through module-7.html) linking directly to sections, concepts,
syntheses, and bibliographies, maintaining semantic HTML and git sync.
"""

from pathlib import Path
import re
import subprocess
import sys


def slugify_heading(title_text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", "", title_text)
    cleaned = re.sub(r"\(.*?\)", "", cleaned)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", cleaned.strip().lower())
    return slug.strip("-")


def add_tocs_to_modules(root_dir: Path) -> None:
    module_files = [root_dir / f"module-{i}.html" for i in range(1, 8)]

    for mod_path in module_files:
        if not mod_path.exists():
            print(f"Skipping {mod_path.name} (not found)")
            continue

        content = mod_path.read_text(encoding="utf-8")

        # Strip any existing in-module TOC card to avoid duplicate insertion
        content = re.sub(r'<nav class="toc-card".*?</nav>\s*', "", content, flags=re.DOTALL)

        # 1. Ensure all h4.concept-title headings have IDs and collect TOC items
        toc_items = []

        def repl_h4(match: re.Match) -> str:
            full_tag = match.group(0)
            text = match.group(1).strip()
            clean_text = re.sub(r"<[^>]+>", "", text)
            slug = slugify_heading(clean_text)
            toc_items.append((slug, clean_text))
            if 'id="' not in full_tag:
                return f'<h4 class="concept-title" id="{slug}">{text}</h4>'
            return full_tag

        content = re.sub(r'<h4 class="concept-title"[^>]*>(.*?)</h4>', repl_h4, content)

        # Check for synthesis boxes and ensure they have IDs
        if 'class="textbook-impact-box"' in content:
            if 'id="critical-synthesis"' not in content:
                content = content.replace(
                    '<div class="textbook-impact-box"',
                    '<div class="textbook-impact-box" id="critical-synthesis"',
                    1,
                )
            toc_items.append(("critical-synthesis", "Critical Synthesis"))

        # Check for bibliography section and ensure it has an ID
        if 'class="biblio-section"' in content:
            if 'id="module-references"' not in content:
                content = content.replace(
                    '<section class="biblio-section"',
                    '<section class="biblio-section" id="module-references"',
                    1,
                )
            toc_items.append(("module-references", "Module References"))

        # 2. Build the Table of Contents HTML block
        list_items_html = "\n".join(
            f'            <li><a href="#{slug}">{label}</a></li>'
            for slug, label in toc_items
        )

        toc_html = f"""
    <!-- MODULE IN-PAGE TABLE OF CONTENTS -->
    <nav class="toc-card" aria-label="Module Table of Contents">
        <h3>Contents in this Module</h3>
        <ul class="toc-grid">
{list_items_html}
        </ul>
    </nav>
"""

        # 3. Insert TOC directly after the intro-card
        if '<div class="intro-card">' in content:
            parts = content.split("</div>", 1)
            # Find the first closing div of the intro card
            intro_end_idx = content.find("</div>", content.find('<div class="intro-card">'))
            if intro_end_idx != -1:
                cut_point = intro_end_idx + len("</div>")
                content = content[:cut_point] + toc_html + content[cut_point:]
        else:
            # Fallback: insert after section heading
            match_h2 = re.search(r"<h2[^>]*>.*?</h2>", content)
            if match_h2:
                cut_point = match_h2.end()
                content = content[:cut_point] + toc_html + content[cut_point:]

        mod_path.write_text(content, encoding="utf-8")
        print(f"Added in-page Table of Contents to {mod_path.name}")


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


def main() -> None:
    root_directory = Path(__file__).resolve().parent
    add_tocs_to_modules(root_directory)

    commit_message = (
        "Add in-page Table of Contents to all seven module pages\n\n"
        "Inject module-level Table of Contents cards directly below intro cards\n"
        "on module-1.html through module-7.html, linking to concept dossiers,\n"
        "syntheses, and references while maintaining citation-free markup."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
