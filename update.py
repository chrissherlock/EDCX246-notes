#!/usr/bin/env python3
"""Clean up core-concepts.html by removing 'Detailed Explanation:' labels."""

from pathlib import Path
import subprocess
import sys


def clean_concepts_file(file_path: Path) -> None:
    if not file_path.exists():
        print(f"Error: Target file '{file_path.resolve()}' not found.", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    # Remove the strong label tag entirely
    cleaned_content = content.replace("<strong>Detailed Explanation:</strong>", "")

    if cleaned_content != content:
        file_path.write_text(cleaned_content, encoding="utf-8")
        print("Successfully stripped 'Detailed Explanation:' labels from core-concepts.html.")
    else:
        print("No matching labels found in core-concepts.html.")


def sync_repository(repo_path: Path) -> None:
    commit_message = (
        "Remove Detailed Explanation label from core-concepts.html\n\n"
        "Strip explanatory prefix tags from concept entries for cleaner formatting."
    )

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
    target_file = root_directory / "core-concepts.html"

    clean_concepts_file(target_file)
    sync_repository(root_directory)


if __name__ == "__main__":
    main()
