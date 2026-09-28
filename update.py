#!/usr/bin/env python3
"""Add linear Back, Home, and Next navigation controls to all module pages

in the EDCX246 revision guide, maintaining semantic HTML and git sync.
"""

from pathlib import Path
import re
import subprocess
import sys

NAV_STYLE = """
        .module-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: 20px 0;
            padding: 10px 0;
            border-top: 1px solid var(--border-subtle, #e7e5e4);
            border-bottom: 1px solid var(--border-subtle, #e7e5e4);
        }
        .nav-btn {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            background-color: var(--bg-banner, #fffbf5);
            border: 1px solid var(--border-accent, #f59e0b);
            border-radius: 6px;
            color: var(--primary-dark, #78350f);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 600;
            transition: background-color 0.15s ease-in-out, color 0.15s ease-in-out;
        }
        .nav-btn:hover {
            background-color: var(--primary, #b45309);
            color: #ffffff;
            border-color: var(--primary, #b45309);
        }
        .nav-btn.disabled {
            opacity: 0.4;
            pointer-events: none;
            cursor: default;
            border-color: var(--border-subtle, #e7e5e4);
        }
"""


def construct_nav_bar(prev_url: str | None, prev_label: str, next_url: str | None, next_label: str) -> str:
    back_html = (
        f'<a href="{prev_url}" class="nav-btn">&larr; {prev_label}</a>'
        if prev_url
        else '<span class="nav-btn disabled">&larr; Previous</span>'
    )
    home_html = '<a href="core-concepts.html" class="nav-btn">&#8962; Home</a>'
    next_html = (
        f'<a href="{next_url}" class="nav-btn">{next_label} &rarr;</a>'
        if next_url
        else '<span class="nav-btn disabled">Next &rarr;</span>'
    )

    return f"""    <nav class="module-nav" aria-label="Module Navigation">
        {back_html}
        {home_html}
        {next_html}
    </nav>"""


def modify_module_files(root_dir: Path) -> None:
    modules = [
        {"file": "module-1.html", "prev": None, "prev_lbl": "", "next": "module-2.html", "next_lbl": "Module 2"},
        {"file": "module-2.html", "prev": "module-1.html", "prev_lbl": "Module 1", "next": "module-3.html", "next_lbl": "Module 3"},
        {"file": "module-3.html", "prev": "module-2.html", "prev_lbl": "Module 2", "next": "module-4.html", "next_lbl": "Module 4"},
        {"file": "module-4.html", "prev": "module-3.html", "prev_lbl": "Module 3", "next": "module-5.html", "next_lbl": "Module 5"},
        {"file": "module-5.html", "prev": "module-4.html", "prev_lbl": "Module 4", "next": "module-6.html", "next_lbl": "Module 6"},
        {"file": "module-6.html", "prev": "module-5.html", "prev_lbl": "Module 5", "next": "module-7.html", "next_lbl": "Module 7"},
        {"file": "module-7.html", "prev": "module-6.html", "prev_lbl": "Module 6", "next": "bibliography.html", "next_lbl": "Bibliography"},
        {"file": "bibliography.html", "prev": "module-7.html", "prev_lbl": "Module 7", "next": None, "next_lbl": ""},
    ]

    for item in modules:
        target = root_dir / item["file"]
        if not target.exists():
            continue

        content = target.read_text(encoding="utf-8")

        # Inject CSS if not already present
        if ".module-nav" not in content:
            content = content.replace("</style>", f"{NAV_STYLE}\n    </style>")

        # Remove standalone legacy back-link anchors
        content = re.sub(r'<a\s+href="core-concepts\.html"\s+class="back-link">.*?</a>\s*', "", content)

        nav_bar = construct_nav_bar(item["prev"], item["prev_lbl"], item["next"], item["next_lbl"])

        # Insert navigation at the top inside <body>
        content = re.sub(r"(<body[^>]*>\s*)", rf"\1\n{nav_bar}\n", content, count=1)

        # Append navigation at the bottom before </body>
        content = re.sub(r"(\s*</body>)", rf"\n{nav_bar}\n\1", content, count=1)

        target.write_text(content, encoding="utf-8")
        print(f"Updated navigation in {item['file']}")


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
    modify_module_files(root_directory)

    commit_message = (
        "Add linear Back, Home, and Next navigation to all modules\n\n"
        "Inject dual top and bottom navigation bars across modules 1 to 7\n"
        "and bibliography.html linking previous, index, and next resources."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
