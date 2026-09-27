#!/usr/bin/env python3
"""Update Symbolic Violence in core-concepts.html to a comprehensive 5-part
diagnostic entry and synchronize via Git.
"""

from pathlib import Path
import re
import subprocess
import sys


def build_symbolic_violence_html() -> str:
    lines = [
        '        <div class="concept-entry">',
        '            <h3>Symbolic Violence (Pierre Bourdieu)</h3>',
        '            <p>Symbolic violence denotes the insidious, non-physical form of domination exerted through the tacit complicity and misrecognition of dominated social agents. It operates when the arbitrary cultural meanings, linguistic codes, and social hierarchies of ruling groups are successfully imposed and internalized as natural, universal, and universally legitimate orders of reality.</p>',
        '',
        '            <p><strong>1. History &amp; The Empirical Anomaly:</strong> The concept was forged by Pierre Bourdieu and Jean-Claude Passeron throughout their empirical work in 1960s Algeria and France, receiving its definitive theoretical exposition in <em>Reproduction in Education, Society and Culture</em> (1970; English 1977) and later in <em>Pascalian Meditations</em> (1997; English 2000). Classical political philosophy struggled with a foundational anomaly: why do stratified societies remain remarkably stable without continuous physical coercion, martial violence, or overt economic bribery? Classical Marxism attributed this stability to crude ideology and "false consciousness" imposed from above, but Bourdieu recognized that ideology models treat agents as passive dupes. Bourdieu observed that subordinate groups actively cooperate in their own subjugation because the cognitive categories and perceptual schemes they use to understand the world are themselves structured by the relations of domination. Power succeeds precisely because it ceases to look like power; it conceals its arbitrary roots and presents itself as natural, neutral common sense.</p>',
        '',
        '            <p><strong>2. Internal Mechanics &amp; Structural Gears:</strong> Bourdieu broke down the apparatus of symbolic violence into several interlocking gears:</p>',
        '            <ul>',
        '                <li><strong>Pedagogic Action &amp; Cultural Arbitrariness:</strong> Every education system transmits a <em>cultural arbitrary</em>—a selective subset of values, knowledge canons, and linguistic registers that reflects the historical interests of dominant groups, yet is presented as universal truth.</li>',
        '                <li><strong>Pedagogic Authority &amp; Legitimate Worth:</strong> Schools wield institutionalized authority that grants them the monopoly on legitimate cultural evaluation. Because this authority is accepted across society, the school can confer moral and intellectual value without appearing partisan or tyrannical.</li>',
        '                <li><strong>Misrecognition (<em>Méconnaissance</em>):</strong> The indispensable cognitive engine of symbolic violence. Subordinate agents recognize the social and educational hierarchy, but <em>misrecognize</em> its arbitrary, class-based origins, believing instead that academic outcomes reflect natural cognitive distributions, genetic ability, or moral industriousness.</li>',
        '                <li><strong>Somatic Inscription:</strong> Symbolic violence is not merely cognitive; it lives in the body. It manifests as visceral sensations of unworthiness, embarrassment, hesitation, posture slumping, and linguistic anxiety when dominated agents interact with dominant institutions.</li>',
        '            </ul>',
        '',
        '            <p><strong>3. Diagnostic Strengths in Schooling:</strong> Symbolic violence provides indispensable diagnostic leverage for exposing how mass education legitimates social inequality:</p>',
        '            <ul>',
        '                <li><em>The Internalization of Personal Failure:</em> When working-class or marginalized students struggle with school curricula, symbolic violence ensures they do not blame the monocultural design of the institution. Instead, they internalize their failure as personal stupidity, lack of effort, or domestic inadequacy, feeling grateful to the system that excludes them.</li>',
        '                <li><em>Neutralizing Conflict:</em> By laundering class privilege through the objective currency of examination results, degrees, and ranking metrics, schools prevent overt class rebellion. Social stratification is effectively depoliticized and recast as fair academic sorting.</li>',
        '                <li><em>Exposing the Paradox of Merit:</em> It unmasks how the most democratic-sounding rhetoric—universal testing, open competitions, blind grading—functions as the ideal vehicle for symbolic domination because it treats unequal competitors as equal, guaranteeing unequal outcomes while manufacturing fairness.</li>',
        '            </ul>',
        '',
        '            <p><strong>4. Critical Vulnerabilities &amp; Blind Spots:</strong> Despite its analytical power, symbolic violence faces serious theoretical and practical critiques:</p>',
        '            <ul>',
        '                <li><em>The Trap of Hyper-Determinism and Fatalism:</em> By asserting that the dominated cannot help but use the oppressor\'s cognitive schemes, Bourdieu\'s framework risks totalizing pessimism. It leaves little conceptual room for genuine counter-hegemonic resistance, radical student consciousness, or emancipatory education.</li>',
        '                <li><em>The Problem of Dominated "Complicity":</em> Calling the dominated "complicit" in their own subordination edges uncomfortably close to paternalism or victim-blaming. Critics like Jacques Rancière argue that this view patronizingly assumes marginalized people are trapped in blindness until enlightened sociologists reveal their subjugation.</li>',
        '                <li><em>Overlooking Resilient Subcultural Defiance:</em> Ethnographies of education (such as Paul Willis\'s working-class lads or modern youth subcultures) demonstrate that marginalized students frequently see through the school\'s arbitrary demands, parodying authority and carving out autonomous cultural dignity rather than meekly absorbing institutional shame.</li>',
        '            </ul>',
        '        </div>'
    ]
    return "\n".join(lines)


def update_core_concepts_file(file_path: Path) -> None:
    if not file_path.exists():
        print(f"Error: Target file '{file_path.resolve()}' not found.", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    pattern = re.compile(
        r'<div class="concept-entry">\s*<h3>Symbolic Violence.*?</div>',
        re.DOTALL
    )

    if not pattern.search(content):
        print("Error: Could not locate Symbolic Violence entry in core-concepts.html.", file=sys.stderr)
        sys.exit(1)

    updated_content = pattern.sub(build_symbolic_violence_html(), content, count=1)
    file_path.write_text(updated_content, encoding="utf-8")
    print(f"Successfully updated Symbolic Violence in: {file_path.resolve()}")


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
    target_file = root_directory / "core-concepts.html"

    update_core_concepts_file(target_file)

    commit_message = (
        "Expand Symbolic Violence into comprehensive 5-part diagnostic entry\n\n"
        "Upgrade the Symbolic Violence section in core-concepts.html with a deep\n"
        "sociological breakdown covering Bourdieu and Passeron's Algerian roots,\n"
        "the mechanics of misrecognition, pedagogic authority, and limits.\n\n"
        "- Detail origins in Algerian fieldwork and Reproduction (1970/1977).\n"
        "- Break down pedagogic action, misrecognition, and cultural arbitrariness.\n"
        "- Analyze the internalization of academic failure and meritocracy traps.\n"
        "- Critique theoretical fatalism and the paradox of dominated complicity."
    )

    execute_git_sync(root_directory, commit_message)


if __name__ == "__main__":
    main()
