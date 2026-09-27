#!/usr/bin/env python3
"""Update index.html to bold 'Attention-Deficit/Hyperactivity Disorder (ADHD):'

in the Chapter 6 neurodevelopmental pedagogical note.
"""

from pathlib import Path
import re
import subprocess
import sys


def apply_adhd_bold_patch(file_path: Path) -> None:
    if not file_path.exists():
        print(f"Error: Target file '{file_path.resolve()}' not found.", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    # Target string to bold
    target_string = "Attention-Deficit/Hyperactivity Disorder (ADHD):"
    replacement_string = "<strong>Attention-Deficit/Hyperactivity Disorder (ADHD):</strong>"

    if target_string in content and replacement_string not in content:
        content = content.replace(target_string, replacement_string, 1)
        print("Successfully bolded Attention-Deficit/Hyperactivity Disorder (ADHD):")
    else:
        print("Target string already bolded or not found in index.html.", file=sys.stderr)

    file_path.write_text(content, encoding="utf-8")
    print(f"Successfully updated and saved: {file_path.resolve()}")


def execute_git_sync(repo_path: Path, commit_message: str) -> None:
    commands = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", commit_message],
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
    target_file = root_directory / "index.html"

    apply_adhd_bold_patch(target_file)

    commit_message = (
        "Bold Attention-Deficit/Hyperactivity Disorder (ADHD): in Chapter 6 note\n\n"
        "Wrap Attention-Deficit/Hyperactivity Disorder (ADHD): in <strong> tags\n"
        "within the neurodevelopmental pedagogical note in index.html.\n\n"
        "- Bold ADHD heading.\n"
        "- Stage changes and push upstream via subprocess."
    )

    execute_git_sync(root_directory, commit_message)


if __name__ == "__main__":
    main()
