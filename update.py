#!/usr/bin/env python3
"""Update Habitus in core-concepts.html to a comprehensive 5-part

diagnostic entry and synchronize via Git.
"""

from pathlib import Path
import re
import subprocess
import sys


def build_habitus_html() -> str:
    return """        <div class="concept-entry">
            <h3>Habitus (Pierre Bourdieu)</h3>
            <p>Habitus denotes a system of durable, transposable dispositions—internalized schemes of perception, appreciation, bodily posture, and action—acquired through sustained immersion in a specific social class and material condition. It functions as a subconscious compass or "feel for the game" (<em>sens pratique</em>), orienting individual choices without requiring conscious rule-following or calculating deliberation.</p>

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> The concept emerged directly from Pierre Bourdieu's ethnographic fieldwork in colonial Algeria during the late 1950s and early 1960s (studying the Kabyle peasants undergoing forced relocation) alongside his sociological studies of rural bachelorhood in his home region of Béarn, France. Bourdieu confronted an acute theoretical impasse between the two dominant intellectual paradigms of mid-twentieth-century France: Claude Lévi-Strauss's <em>structuralism</em> (which reduced human agents to passive automatons executing rigid, unconscious cultural rules) and Jean-Paul Sartre's <em>existentialism</em> (which posited radical, unconstrained personal freedom and sovereign choice). Neither model could explain what Bourdieu observed in Algeria: displaced peasants could not simply "choose" to become capitalist wage-earners overnight, nor were they merely following mechanical scripts. Instead, their traditional rural dispositions, temporal rhythms, and economic assumptions clashed fundamentally with the colonial monetary economy. To transcend this objectivist/subjectivist dualism, Bourdieu retrieved the classical Aristotelian concept of <em>hexis</em> (moral character acquired through bodily habit), passed through medieval scholasticism via Thomas Aquinas as <em>habitus</em>, and sociological antecedents in Marcel Mauss's bodily techniques. He codified habitus in <em>Outline of a Theory of Practice</em> (1972; English 1977) and <em>The Logic of Practice</em> (1980) as a generative apparatus bridging objective social structures and subjective human action.</p>

            <p><strong>2. Internal Mechanics &amp; Generative Gears:</strong> Bourdieu defined habitus through a famous formulation: <em>"structured structures predisposed to function as structuring structures."</em> This mechanism operates on two interconnected levels:</p>
            <ul>
                <li><strong>A Structured Structure (Internalized Social Reality):</strong> Early childhood socialization within a specific material condition internalizes the objective probabilities, boundaries, and limits of that class position into deep-seated mental schemas. What is objectively impossible or rare for a social group is experienced internally as unthinkable or undesirable.</li>
                <li><strong>A Structuring Structure (Generative Action):</strong> Habitus is not a rigid cage, but an open generative grammar (analogous to Chomsky's linguistic competence) that produces an infinite variety of improvisational practices, thoughts, tastes, and choices—all constrained within the unspoken boundaries of its originating class conditions.</li>
                <li><strong>Bodily Hexis:</strong> Habitus is thoroughly somaticized. It lives in the body as "political mythology turned into a physical demeanor"—manifested in posture, vocal modulation, physical stance, laughter, walking gait, and relationship to physical space.</li>
            </ul>

            <p><strong>3. Diagnostic Strengths in Schooling:</strong> Habitus provides extraordinary diagnostic power for deciphering the informal, psychological sorting mechanisms of mass education:</p>
            <ul>
                <li><em>Institutional Affinity vs. Dislocation:</em> When a middle-class student enters formal schooling, their home habitus aligns organically with the institutional habitus of the school. They move through classrooms "like a fish in water," intuitively understanding conversational cadences, teacher expectations, and unwritten cultural codes. Conversely, working-class students experience visceral cultural dislocation, feeling clumsy, scrutinized, and out of place.</li>
                <li><em>Explaining Self-Elimination:</em> Habitus unmasks how educational sorting occurs without visible coercion. Rather than schools actively expelling working-class youth, students perform self-selection and self-elimination, adopting attitudes such as <em>"that's not for the likes of us"</em> or viewing academic tracking as personal choice. Objective institutional barriers are translated into internalized subjective limits.</li>
                <li><em>Explaining Compliance Without Conspiracy:</em> It demonstrates how teachers and administrators reproduce systemic class inequalities without harboring overt class prejudice or conscious malicious intent, simply by acting upon their own deeply ingrained, naturalized dispositions.</li>
            </ul>

            <p><strong>4. Critical Vulnerabilities &amp; Blind Spots:</strong> Despite its analytical brilliance, habitus faces substantial theoretical and operational critique:</p>
            <ul>
                <li><em>The Trap of Circular Determinism:</em> Critics (including Anthony Giddens and Jacques Rancière) argue that Bourdieu's formulation risks circular fatalism: past conditions produce the habitus, which generates practices that inevitably reproduce the original conditions. This over-socialized view struggles to account for genuine upward social mobility, radical counter-hegemonic political action, or intentional reinvention.</li>
                <li><em>The "Hysteresis Effect" and Rapid Change:</em> Bourdieu coined the term <em>hysteresis</em> (or the "Don Quixote effect") to describe the temporal lag when an individual's habitus remains calibrated to past conditions that no longer match the changing objective structures of the field. However, in hyper-dynamic, digitally mediated societies, dispositions adapt far more rapidly and heterogeneously than a static, lifelong habitus model allows.</li>
                <li><em>Reflexivity in Modern Learners:</em> Contemporary educational sociologists argue that diverse, multicultural, and modern youth routinely exhibit cross-cultural reflexivity—consciously code-switching and deploying multiple, fragmented "habitus repertoires" rather than remaining bound to a singular, monolithic class disposition.</li>
            </ul>
        </div>"""


def update_core_concepts_file(file_path: Path) -> None:
    if not file_path.exists():
        print(f"Error: Target file '{file_path.resolve()}' not found.", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    # Match the entire Habitus concept-entry block
    pattern = re.compile(
        r'<div class="concept-entry">\s*<h3>Habitus.*?</div>',
        re.DOTALL
    )

    if not pattern.search(content):
        print("Error: Could not locate Habitus entry in core-concepts.html.", file=sys.stderr)
        sys.exit(1)

    updated_content = pattern.sub(build_habitus_html(), content, count=1)
    file_path.write_text(updated_content, encoding="utf-8")
    print(f"Successfully updated Habitus in: {file_path.resolve()}")


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
        "Expand Habitus into comprehensive 5-part diagnostic entry\n\n"
        "Upgrade the Habitus section in core-concepts.html with a deep\n"
        "sociological breakdown covering Bourdieu's Algerian ethnographic roots,\n"
        "the critique of structuralism and existentialism, generative bodily hexis,\n"
        "and critical limitations.\n\n"
        "- Detail origins in 1950s/60s Algerian fieldwork and Béarn studies.\n"
        "- Break down structured structure, structuring structure, and bodily hexis.\n"
        "- Analyze institutional affinity, self-elimination, and schooling outcomes.\n"
        "- Critique circular determinism and the hysteresis effect."
    )

    execute_git_sync(root_directory, commit_message)


if __name__ == "__main__":
    main()
