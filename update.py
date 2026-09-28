#!/usr/bin/env python3
"""Add a navigation link back to index.html at the top of core-concepts.html

and sync the changes via git.
"""

from pathlib import Path
import subprocess
import sys


def inject_index_link(root_dir: Path) -> None:
    target = root_dir / "core-concepts.html"
    if not target.exists():
        print("core-concepts.html not found.")
        return

    content = target.read_text(encoding="utf-8")

    back_link_html = """    <nav style="margin-bottom: 20px;">
        <a href="index.html" style="display: inline-flex; align-items: center; padding: 6px 12px; background-color: #fff7ed; border: 1px solid #fdba74; border-radius: 5px; color: #78350f; text-decoration: none; font-size: 0.88rem; font-weight: 600;">&larr; Back to Main Overview</a>
    </nav>"""

    if 'href="index.html"' not in content:
        # Insert right after <body>
        content = content.replace("<body>", f"<body>\n{back_link_html}")
        target.write_text(content, encoding="utf-8")
        print("Added link back to index.html in core-concepts.html")
    else:
        print("Link back to index.html already present in core-concepts.html")


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
    inject_index_link(root_directory)

    commit_message = (
        "Add link back to root index.html on core-concepts.html portal\n\n"
        "Insert a clean navigation link at the top of core-concepts.html\n"
        "pointing back to the main overview page (index.html)."
    )

    execute_git_sync(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
