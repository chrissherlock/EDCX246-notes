#!/usr/bin/env python3
"""Update core-concepts.html to provide a more detailed and enriched

academic explanation for Cultural Capital.
"""

from pathlib import Path
import re
import subprocess
import sys


def update_cultural_capital_explanation(file_path: Path) -> None:
    if not file_path.exists():
        print(f"Error: Target file '{file_path.resolve()}' not found.", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    # Target block for Cultural Capital to update
    target_block = re.compile(
        r'(<h3>Cultural Capital</h3>\s*<p>)<strong>Detailed Explanation:</strong>.*?(</p>\s*<p>)<strong>Operational Role in Schooling:</strong>.*?(</p>)',
        re.DOTALL
    )

    enriched_html = (
        r'\1<strong>Detailed Explanation:</strong> Originally theorized by French sociologist Pierre Bourdieu '
        r'in works such as <em>Reproduction in Education, Society and Culture</em>, cultural capital refers to '
        r'the non-financial social assets that an individual inherits, accumulates, and deploys to navigate social '
        r'structures. Bourdieu categorized these assets into three distinct forms: <em>embodied</em> (long-lasting '
        r'dispositions of mind and body, including linguistic fluency, posture, and cultural competence), <em>objectified</em> '
        r'(cultural goods such as books, instruments, artworks, and digital artifacts), and <em>institutionalized</em> '
        r'(legally recognized academic credentials and degrees that confer formal market value).<br><br>'
        r'Crucially, cultural capital is not a measure of individual intelligence or absolute moral worth; rather, '
        r'it is an acquired class-based currency that grants distinct competitive advantages in hierarchical social fields.\2'
        r'<strong>Operational Role in Schooling:</strong> Mainstream schooling operates on the structural fiction of '
        r'formal neutrality and universal meritocracy. In practice, however, educational institutions implicitly '
        r'demand and reward the specific linguistic codes, aesthetic preferences, and interaction styles associated '
        r'with the middle and ruling classes.<br><br>'
        r'When working-class students enter the classroom equipped with different, yet equally rich, vernaculars and '
        r'forms of cultural knowledge, schools systematically <em>misrecognize</em> their inherited disadvantage as '
        r'innate intellectual deficit or lack of motivation. By treating dominant cultural capital as the universal '
        r'yardstick of "merit," schools commit <strong>symbolic violence</strong>—legitimating class inequality and '
        r'transmitting privilege across generations under the disarming guise of objective academic success.\3'
    )

    if target_block.search(content):
        content = target_block.sub(enriched_html, content, count=1)
        print("Successfully updated Cultural Capital explanation in core-concepts.html.")
    else:
        print("Error: Could not locate the Cultural Capital block in core-concepts.html.", file=sys.stderr)
        sys.exit(1)

    file_path.write_text(content, encoding="utf-8")
    print(f"Successfully saved updated file: {file_path.resolve()}")


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
    target_file = root_directory / "core-concepts.html"

    update_cultural_capital_explanation(target_file)

    commit_message = (
        "Update Cultural Capital explanation in core-concepts.html\n\n"
        "Provide a detailed academic breakdown of Bourdieu's three forms of cultural\n"
        "capital (embodied, objectified, institutionalized) and its institutional role\n"
        "in misrecognition and symbolic violence.\n\n"
        "- Expand Cultural Capital section with rigorous theoretical depth.\n"
        "- Stage changes and push upstream via subprocess."
    )

    execute_git_sync(root_directory, commit_message)


if __name__ == "__main__":
    main()
