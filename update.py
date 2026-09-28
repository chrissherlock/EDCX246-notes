#!/usr/bin/env python3
"""Modernize and refine the visual styling of in-page Tables of Contents

across module-1.html through module-7.html, replacing plain lists with an
elevated card interface, numbered chip items, and smooth hover dynamics.
"""

from pathlib import Path
import re
import subprocess
import sys

REFINED_TOC_CSS = """
        /* Modernized Sophisticated Table of Contents */
        .toc-card {
            background: linear-gradient(180deg, #fffcf8 0%, #faf5ec 100%);
            border: 1px solid #e7ded0;
            border-left: 4px solid var(--accent-orange, #ea580c);
            border-radius: 8px;
            padding: 18px 22px 20px 22px;
            margin: 20px 0 28px 0;
            box-shadow: 0 2px 8px rgba(120, 53, 15, 0.04);
        }
        .toc-header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
            padding-bottom: 8px;
            border-bottom: 1px dashed #e7ded0;
        }
        .toc-card h3 {
            font-size: 0.95rem;
            color: var(--primary-dark, #78350f);
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .toc-badge {
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--accent-orange, #ea580c);
            background: #ffedd5;
            padding: 2px 8px;
            border-radius: 12px;
            letter-spacing: 0.02em;
        }
        .toc-grid {
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 8px 12px;
        }
        .toc-grid li {
            margin: 0;
            padding: 0;
            font-size: 0.88rem;
        }
        .toc-grid a {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 7px 12px;
            background: #ffffff;
            border: 1px solid #ebdccb;
            border-radius: 6px;
            color: var(--text-main, #292524);
            text-decoration: none;
            font-weight: 600;
            transition: all 0.15s ease-in-out;
        }
        .toc-item-label {
            display: flex;
            align-items: center;
            gap: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .toc-index {
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--primary, #b45309);
            opacity: 0.85;
            font-variant-numeric: tabular-nums;
        }
        .toc-chevron {
            font-size: 0.82rem;
            color: #a8a29e;
            transition: transform 0.15s ease-in-out, color 0.15s ease-in-out;
            margin-left: 6px;
        }
        .toc-grid a:hover {
            color: var(--primary-dark, #78350f);
            border-color: var(--border-accent, #f59e0b);
            background: #fffdf9;
            transform: translateY(-1.5px);
            box-shadow: 0 3px 8px rgba(180, 83, 9, 0.08);
        }
        .toc-grid a:hover .toc-chevron {
            color: var(--accent-orange, #ea580c);
            transform: translateX(2px);
        }
"""


def slugify_heading(title_text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", "", title_text)
    cleaned = re.sub(r"\(.*?\)", "", cleaned)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", cleaned.strip().lower())
    return slug.strip("-")


def modernize_module_tocs(root_dir: Path) -> None:
    module_files = [root_dir / f"module-{i}.html" for i in range(1, 8)]

    for mod_path in module_files:
        if not mod_path.exists():
            continue

        content = mod_path.read_text(encoding="utf-8")

        # 1. Update or inject CSS
        if ".toc-item-label" not in content:
            if ".toc-card {" in content:
                # Replace legacy .toc-card block up to .forensic-entry
                content = re.sub(
                    r"/\* Table of Contents Styling \*/\s*\.toc-card\s*\{.*?(?=\.forensic-entry)",
                    f"{REFINED_TOC_CSS}\n        ",
                    content,
                    flags=re.DOTALL,
                )
            else:
                content = content.replace("</style>", f"{REFINED_TOC_CSS}\n    </style>")

        # 2. Gather entries dynamically
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

        if 'class="textbook-impact-box"' in content:
            if 'id="critical-synthesis"' not in content:
                content = content.replace(
                    '<div class="textbook-impact-box"',
                    '<div class="textbook-impact-box" id="critical-synthesis"',
                    1,
                )
            toc_items.append(("critical-synthesis", "Critical Synthesis"))

        if 'class="biblio-section"' in content:
            if 'id="module-references"' not in content:
                content = content.replace(
                    '<section class="biblio-section"',
                    '<section class="biblio-section" id="module-references"',
                    1,
                )
            toc_items.append(("module-references", "Module References"))

        # 3. Build refined Table of Contents markup
        total_items = len(toc_items)
        items_markup = []
        for idx, (slug, label) in enumerate(toc_items, start=1):
            num_str = f"{idx:02d}"
            item_html = (
                f'            <li>\n'
                f'                <a href="#{slug}">\n'
                f'                    <span class="toc-item-label">\n'
                f'                        <span class="toc-index">{num_str}</span>\n'
                f'                        <span>{label}</span>\n'
                f'                    </span>\n'
                f'                    <span class="toc-chevron">&rarr;</span>\n'
                f'                </a>\n'
                f'            </li>'
            )
            items_markup.append(item_html)

        list_block = "\n".join(items_markup)

        refined_toc_html = f"""
    <!-- REFINED MODULE IN-PAGE TABLE OF CONTENTS -->
    <nav class="toc-card" aria-label="Module Quick Index">
        <div class="toc-header-row">
            <h3>Quick Navigation</h3>
            <span class="toc-badge">{total_items} Sections</span>
        </div>
        <ul class="toc-grid">
{list_block}
        </ul>
    </nav>
"""

        # 4. Replace existing TOC or insert after intro-card
        if '<!-- MODULE IN-PAGE TABLE OF CONTENTS -->' in content:
            content = re.sub(
                r'<!-- MODULE IN-PAGE TABLE OF CONTENTS -->\s*<nav class="toc-card".*?</nav>',
                refined_toc_html.strip(),
                content,
                flags=re.DOTALL,
            )
        elif '<!-- REFINED MODULE IN-PAGE TABLE OF CONTENTS -->' in content:
            content = re.sub(
                r'<!-- REFINED MODULE IN-PAGE TABLE OF CONTENTS -->\s*<nav class="toc-card".*?</nav>',
                refined_toc_html.strip(),
                content,
                flags=re.DOTALL,
            )
        elif '<nav class="toc-card"' in content:
            content = re.sub(
                r'<nav class="toc-card".*?</nav>',
                refined_toc_html.strip(),
                content,
                flags=re.DOTALL,
            )
        else:
            intro_end = content.find("</div>", content.find('<div class="intro-card">'))
            if intro_end != -1:
                cut_point = intro_end + len("</div>")
                content = content[:cut_point] + refined_toc_html + content[cut_point:]

        mod_path.write_text(content, encoding="utf-8")
        print(f"Upgraded TOC styling in {mod_path.name}")


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
    modernize_module_tocs(root_directory)

    commit_message = (
        "Refine and modernize in-page Table of Contents styling\n\n"
        "Replace plain text lists with an elevated index surface featuring\n"
        "interactive numbered chips, smooth hover elevation, and responsive\n"
        "grid alignment across module-1.html through module-7.html."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
