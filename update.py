#!/usr/bin/env python3
"""Replace blocky card-based TOC styling with a light, typographic editorial

index layout across all module pages.
"""

from pathlib import Path
import re
import subprocess
import sys

EDITORIAL_TOC_CSS = """
        /* Editorial Table of Contents */
        .toc-card {
            background: transparent;
            border: none;
            border-top: 1px solid #fed7aa;
            border-bottom: 1px solid #fed7aa;
            border-radius: 0;
            padding: 16px 0 20px 0;
            margin: 24px 0 34px 0;
            box-shadow: none;
        }
        .toc-header-row {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 0;
            border-bottom: none;
        }
        .toc-card h3 {
            font-size: 0.78rem;
            color: var(--primary);
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-weight: 700;
        }
        .toc-badge {
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-muted);
            background: none;
            padding: 0;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .toc-grid {
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 6px 32px;
        }
        .toc-grid li {
            margin: 0;
            padding: 0;
        }
        .toc-grid a {
            display: flex;
            align-items: baseline;
            gap: 10px;
            padding: 4px 0;
            background: transparent;
            border: none;
            border-bottom: 1px solid transparent;
            border-radius: 0;
            color: var(--text-main);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 500;
            transition: color 0.15s ease-in-out, border-color 0.15s ease-in-out;
        }
        .toc-item-label {
            display: inline;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .toc-index {
            font-size: 0.75rem;
            font-weight: 700;
            font-family: -apple-system, BlinkMacSystemFont, "SF Mono", Menlo, monospace;
            color: var(--primary);
            opacity: 0.7;
            flex-shrink: 0;
        }
        .toc-chevron {
            display: none;
        }
        .toc-grid a:hover {
            color: var(--accent-orange);
            background: transparent;
            transform: none;
            box-shadow: none;
            border-bottom: 1px dotted var(--accent-orange);
        }
"""


def apply_editorial_toc(root_dir: Path) -> None:
    module_files = [root_dir / f"module-{i}.html" for i in range(1, 8)]

    for mod_path in module_files:
        if not mod_path.exists():
            continue

        content = mod_path.read_text(encoding="utf-8")

        # Replace existing .toc-card CSS rule block
        if ".toc-card {" in content:
            content = re.sub(
                r"/\*.*?\*/\s*\.toc-card\s*\{.*?(?=\.forensic-entry|\.diagram-container|\.counter-svg-container|\.module-nav|</style>)",
                f"{EDITORIAL_TOC_CSS}\n        ",
                content,
                flags=re.DOTALL,
            )
            mod_path.write_text(content, encoding="utf-8")
            print(f"Updated TOC styling to editorial mode in {mod_path.name}")


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
    apply_editorial_toc(root_directory)

    commit_message = (
        "Switch module Tables of Contents to editorial typographic styling\n\n"
        "Replace card-based pill layout with a clean hairline rule system,\n"
        "tabular index numbering, and subtle text hover effects."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
