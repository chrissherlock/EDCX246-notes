#!/usr/bin/env python3
"""Update Cultural Capital in core-concepts.html to a comprehensive 5-part

diagnostic entry and synchronize via Git.
"""

from pathlib import Path
import re
import subprocess
import sys


def build_cultural_capital_html() -> str:
    return """        <div class="concept-entry">
            <h3>Cultural Capital (Pierre Bourdieu)</h3>
            <p>Cultural capital represents the non-financial social assets—embodied linguistic fluency, academic mannerisms, aesthetic dispositions, and formal credentials—that individuals inherit through class socialization and deploy to navigate social hierarchies. Rather than reflecting innate cognitive ability, it operates as an institutionalized class currency that educational systems covertly demand and reward.</p>

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> The concept emerged from empirical investigations conducted across post-WWII French education during the 1960s by Pierre Bourdieu and Jean-Claude Passeron. State technocrats had eliminated university tuition fees, anticipating that open financial access would establish a pure meritocracy. However, statistical surveys revealed a glaring contradiction: despite free tuition, working-class and peasant students continued to fail and drop out at drastically higher rates than bourgeois cohorts. Classical Marxist theory attributed class reproduction almost exclusively to economic capital (property, wealth, and ownership of the means of production), but Bourdieu recognized that financial explanations could not account for why working-class students with adequate funding still struggled with the implicit cultural demands of the academy. To resolve this breakdown, Bourdieu expanded the definition of capital beyond economics into the cultural realm, demonstrating that schools trade in cultural wealth. The term was formally introduced in print in the 1973 essay <em>Cultural Reproduction and Social Reproduction</em> and later codified into its three distinct states in the 1986 essay <em>The Forms of Capital</em>.</p>

            <p><strong>2. Internal Mechanics &amp; Three States:</strong> Bourdieu established that cultural capital exists and circulates in three interrelated states:</p>
            <ul>
                <li><strong>Embodied State (<em>État Incorporé</em>):</strong> Long-lasting dispositions of the mind and body. This encompasses linguistic syntax, ease with abstract concepts, pronunciation, bodily posture, aesthetic tastes, and conversational confidence. Embodied capital cannot be transmitted overnight or purchased as a commodity; it requires slow, subconscious habituation through early family socialization.</li>
                <li><strong>Objectified State (<em>État Objectivé</em>):</strong> Cultural goods and physical artifacts—such as classical literature, scientific instruments, scholarly libraries, artwork, and technological tools. While these goods can be bought with money, their academic utility requires the prerequisite embodied capital needed to decode and appreciate them.</li>
                <li><strong>Institutionalized State (<em>État Institutionalisé</em>):</strong> Formally certified academic degrees, diplomas, and credentials. This state converts embodied competence into state-recognized currency with guaranteed exchange value in the labor market, allowing elites to convert cultural fluency into economic reward.</li>
            </ul>
            <p>Crucially, cultural capital operates in relation to a <em>field</em> (a structured social arena of competition). In the educational field, middle- and upper-class cultural capital is treated as the natural, universal standard of competence.</p>

            <p><strong>3. Diagnostic Strengths in Schooling:</strong> The concept provides immense explanatory leverage by exposing the structural mechanics of educational reproduction:</p>
            <ul>
                <li><em>Dismantling the Meritocracy Myth:</em> It reveals that academic success is largely the conversion of inherited cultural familiarity into academic merit.</li>
                <li><em>Unmasking Misrecognition and Symbolic Violence:</em> Schools systematically misrecognize inherited class advantages as innate intellectual brilliance, while treating working-class vernaculars and cultural knowledge as cognitive deficits. By compelling marginalized students to internalize failure as personal inadequacy, schools commit symbolic violence.</li>
                <li><em>Explaining Policy Inadequacy:</em> It demonstrates why purely material interventions (vouchers, fee waivers, hardware rollouts) consistently fail to close equity gaps if the implicit cultural expectations of curricula and assessments remain unexamined.</li>
            </ul>

            <p><strong>4. Critical Vulnerabilities &amp; Blind Spots:</strong> Despite its diagnostic power, the concept possesses significant theoretical limitations:</p>
            <ul>
                <li><em>Structural Fatalism:</em> Bourdieu's model operates as an almost unbroken cycle of reproduction, leaving little room for student agency, social mobility, or the documented ability of transformative teachers to break intergenerational disadvantage.</li>
                <li><em>The "Delpit Dilemma" &amp; Relativism:</em> Characterizing standard academic English, formal rhetoric, and abstract mathematics purely as arbitrary ruling-class power tools risks sliding into anti-intellectual relativism. As educational scholar Lisa Delpit argues, disadvantaged students already possess rich local vernaculars; what they require from public education is explicit, systematic instruction in the "culture of power" and powerful disciplinary knowledge to achieve social mobility, not romantic validation that leaves them excluded from university access.</li>
                <li><em>Empirical Quantification:</em> Unlike financial wealth, cultural capital is notoriously difficult to isolate and quantify, occasionally blurring into circular reasoning where academic success is explained by cultural capital, and cultural capital is proven by academic success.</li>
            </ul>
        </div>"""


def update_core_concepts_file(file_path: Path) -> None:
    if not file_path.exists():
        print(f"Error: Target file '{file_path.resolve()}' not found.", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    # Match the entire Cultural Capital concept-entry block
    pattern = re.compile(
        r'<div class="concept-entry">\s*<h3>Cultural Capital.*?</div>',
        re.DOTALL
    )

    if not pattern.search(content):
        print("Error: Could not locate Cultural Capital entry in core-concepts.html.", file=sys.stderr)
        sys.exit(1)

    updated_content = pattern.sub(build_cultural_capital_html(), content, count=1)
    file_path.write_text(updated_content, encoding="utf-8")
    print(f"Successfully updated Cultural Capital in: {file_path.resolve()}")


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
        "Expand Cultural Capital into comprehensive 5-part diagnostic entry\n\n"
        "Upgrade the Cultural Capital section in core-concepts.html with a full\n"
        "sociological breakdown covering its post-WWII empirical origins, the\n"
        "three states of capital, field conversion, and critical blind spots.\n\n"
        "- Trace historical genesis from post-WWII France to 1973/1986 works.\n"
        "- Define embodied, objectified, and institutionalized capital states.\n"
        "- Analyze institutional misrecognition and symbolic violence in schools.\n"
        "- Critique theoretical fatalism and the Delpit Dilemma."
    )

    execute_git_sync(root_directory, commit_message)


if __name__ == "__main__":
    main()
