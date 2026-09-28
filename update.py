#!/usr/bin/env python3
"""Append dedicated, module-specific bibliographies to the end of each module

page (module-1.html through module-7.html), ensuring self-contained scholarly
references, semantic HTML formatting, and automated git synchronization.
"""

from pathlib import Path
import re
import subprocess
import sys

MODULE_BIBLIOGRAPHIES = {
    "module-1.html": """
    <section class="biblio-section">
        <h2>Module 1 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Bernstein, B. (1971).</strong> <em>Class, Codes and Control: Volume 1, Theoretical Studies Towards a Sociology of Language</em>. London: Routledge &amp; Kegan Paul.</li>
            <li><strong>Bourdieu, P. (1973).</strong> 'Cultural Reproduction and Social Reproduction'. In R. Brown (Ed.), <em>Knowledge, Education, and Cultural Change: Papers in the Sociology of Education</em> (pp. 71–112). London: Tavistock Publications.</li>
            <li><strong>Bourdieu, P. (1977).</strong> <em>Outline of a Theory of Practice</em> (R. Nice, Trans.). Cambridge: Cambridge University Press. (Original work published in French 1972).</li>
            <li><strong>Bourdieu, P. (1984).</strong> <em>Distinction: A Social Critique of the Judgement of Taste</em> (R. Nice, Trans.). Cambridge, MA: Harvard University Press. (Original work published in French 1979).</li>
            <li><strong>Bourdieu, P. (1986).</strong> 'The Forms of Capital'. In J. G. Richardson (Ed.), <em>Handbook of Theory and Research for the Sociology of Education</em> (pp. 241–258). New York: Greenwood Press.</li>
            <li><strong>Bourdieu, P. (1990).</strong> <em>The Logic of Practice</em> (R. Nice, Trans.). Stanford: Stanford University Press.</li>
            <li><strong>Bourdieu, P., &amp; Passeron, J.-C. (1977).</strong> <em>Reproduction in Education, Society and Culture</em> (R. Nice, Trans.). London: Sage Publications. (Original work published in French 1970).</li>
            <li><strong>Bourdieu, P. (2000).</strong> <em>Pascalian Meditations</em> (R. Nice, Trans.). Stanford: Stanford University Press. (Original work published in French 1997).</li>
            <li><strong>Collins, R. (1979).</strong> <em>The Credential Society: An Historical Sociology of Education and Stratification</em>. New York: Academic Press.</li>
            <li><strong>Delpit, L. (1988).</strong> 'The Silenced Dialogue: Power and Pedagogy in Educating Other People's Children'. <em>Harvard Educational Review</em>, 58(3), 280–298.</li>
            <li><strong>Delpit, L. (1995).</strong> <em>Other People's Children: Cultural Conflict in the Classroom</em>. New York: The New Press.</li>
            <li><strong>Labov, W. (1972).</strong> <em>Language in the Inner City: Studies in the Black English Vernacular</em>. Philadelphia: University of Pennsylvania Press.</li>
            <li><strong>Rancière, J. (2004).</strong> <em>The Philosopher and His Poor</em> (J. Drury, C. Oster, &amp; A. Parker, Trans.). Durham, NC: Duke University Press. (Original work published in French 1983).</li>
            <li><strong>Vinson, T. (2002).</strong> <em>Inquiry into the Provision of Public Education in New South Wales</em>. Sydney: NSW Teachers Federation &amp; Principals' Councils.</li>
            <li><strong>Weber, M. (1978).</strong> <em>Economy and Society: An Outline of Interpretive Sociology</em> (G. Roth &amp; C. Wittich, Eds.). Berkeley: University of California Press. (Original work published 1922).</li>
            <li><strong>Willis, P. (1977).</strong> <em>Learning to Labour: How Working Class Kids Get Working Class Jobs</em>. Farnborough: Saxon House.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
        </ul>
    </section>
""",
    "module-2.html": """
    <section class="biblio-section">
        <h2>Module 2 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Achebe, C. (1975).</strong> <em>Morning Yet on Creation Day: Essays</em>. London: Heinemann.</li>
            <li><strong>Bell, D. A. (1980).</strong> 'Brown v. Board of Education and the Interest-Convergence Dilemma'. <em>Harvard Law Review</em>, 93(3), 518–533.</li>
            <li><strong>Delpit, L. (1995).</strong> <em>Other People's Children: Cultural Conflict in the Classroom</em>. New York: The New Press.</li>
            <li><strong>Fanon, F. (1963).</strong> <em>The Wretched of the Earth</em> (C. Farrington, Trans.). New York: Grove Press. (Original work published in French 1961).</li>
            <li><strong>Fanon, F. (1967).</strong> <em>Black Skin, White Masks</em> (C. L. Markmann, Trans.). New York: Grove Press. (Original work published in French 1952).</li>
            <li><strong>Fricker, M. (2007).</strong> <em>Epistemic Injustice: Power and the Ethics of Knowing</em>. Oxford: Oxford University Press.</li>
            <li><strong>Gillborn, D. (2005).</strong> 'Education policy as an act of white supremacy: Whiteness, critical race theory and education reform'. <em>Journal of Education Policy</em>, 20(4), 485–505.</li>
            <li><strong>Gillborn, D. (2008).</strong> <em>Racism and Education: Coincidence or Conspiracy?</em> London: Routledge.</li>
            <li><strong>Ladson-Billings, G. (1995).</strong> 'Toward a Theory of Culturally Relevant Pedagogy'. <em>American Educational Research Journal</em>, 32(3), 465–491.</li>
            <li><strong>Macaulay, T. B. (1835).</strong> <em>Minute on Indian Education</em>. London: British Parliamentary Papers.</li>
            <li><strong>Macpherson, W. (1999).</strong> <em>The Stephen Lawrence Inquiry: Report of an Inquiry by Sir William Macpherson of Cluny</em>. London: The Stationery Office.</li>
            <li><strong>Ngũgĩ wa Thiong'o. (1986).</strong> <em>Decolonising the Mind: The Politics of Language in African Literature</em>. London: James Currey.</li>
            <li><strong>Paris, D. (2012).</strong> 'Culturally Sustaining Pedagogy: A Needed Change in Stance, Terminology, and Practice'. <em>Educational Researcher</em>, 41(3), 93–97.</li>
            <li><strong>Paris, D., &amp; Alim, H. S. (2014).</strong> 'What Are We Seeking to Sustain Through Culturally Sustaining Pedagogy? A Loving Critique Forward'. <em>Harvard Educational Review</em>, 84(1), 85–100.</li>
            <li><strong>Paris, D., &amp; Alim, H. S. (Eds.). (2017).</strong> <em>Culturally Sustaining Pedagogies: Teaching and Learning for Justice in a Changing World</em>. New York: Teachers College Press.</li>
            <li><strong>Sewell, T. (2021).</strong> <em>Commission on Race and Ethnic Disparities: The Report</em>. London: UK Cabinet Office.</li>
            <li><strong>Spivak, G. C. (1988).</strong> 'Can the Subaltern Speak?' In C. Nelson &amp; L. Grossberg (Eds.), <em>Marxism and the Interpretation of Culture</em> (pp. 271–313). Urbana: University of Illinois Press.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
        </ul>
    </section>
""",
    "module-3.html": """
    <section class="biblio-section">
        <h2>Module 3 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Butler, J. (1990).</strong> <em>Gender Trouble: Feminism and the Subversion of Identity</em>. New York: Routledge.</li>
            <li><strong>Butler, J. (1993).</strong> <em>Bodies That Matter: On the Discursive Limits of "Sex"</em>. New York: Routledge.</li>
            <li><strong>Connell, R. W. (1987).</strong> <em>Gender and Power: Society, the Person and Sexual Politics</em>. Stanford: Stanford University Press.</li>
            <li><strong>Connell, R. W. (1995).</strong> <em>Masculinities</em>. Berkeley: University of California Press.</li>
            <li><strong>Connell, R. W. (2000).</strong> <em>The Men and the Boys</em>. Berkeley: University of California Press.</li>
            <li><strong>Demetriou, D. Z. (2001).</strong> 'Connell's Concept of Hegemonic Masculinity: A Critique'. <em>Theory and Society</em>, 30(3), 337–361.</li>
            <li><strong>Ferguson, A., Gottschalk, P. H., Campbell, B. B., &amp; Rich, A. (1981).</strong> 'On "Compulsory Heterosexuality and Lesbian Existence": Defining the Issues'. <em>Signs: Journal of Women in Culture and Society</em>, 7(1), 158–199.</li>
            <li><strong>Kosciw, J. G., Clark, C. M., Truong, N. L., &amp; Zongrone, A. D. (2020).</strong> <em>The 2019 National School Climate Survey: The Experiences of Lesbian, Gay, Bisexual, Transgender, and Queer Youth in Our Nation's Schools</em>. New York: GLSEN.</li>
            <li><strong>Mac an Ghaill, M. (1994).</strong> <em>The Making of Men: Masculinities, Sexualities and Schooling</em>. Buckingham: Open University Press.</li>
            <li><strong>Mayo, C. (2014).</strong> <em>LGBTQ Youth and Education: Policies and Practices</em>. New York: Teachers College Press.</li>
            <li><strong>Meyer, I. H. (2003).</strong> 'Prejudice, Social Stress, and Mental Health in Lesbian, Gay, and Bisexual Populations: Conceptual Issues and Research Evidence'. <em>Psychological Bulletin</em>, 129(5), 674–697.</li>
            <li><strong>Nussbaum, M. (1999).</strong> 'The Professor of Parody: The Hip Defeatism of Judith Butler'. <em>The New Republic</em>, 220(8), 37–45.</li>
            <li><strong>Rich, A. (1980).</strong> 'Compulsory Heterosexuality and Lesbian Existence'. <em>Signs: Journal of Women in Culture and Society</em>, 5(4), 631–660.</li>
            <li><strong>Ullman, J. (2021).</strong> <em>Free to Be? Exploring the Schooling Experiences of Australia's Sexuality and Gender Diverse High School Students</em>. Penrith: Western Sydney University.</li>
            <li><strong>Warner, M. (1993).</strong> <em>Fear of a Queer Planet: Queer Politics and Social Theory</em>. Minneapolis: University of Minnesota Press.</li>
        </ul>
    </section>
""",
    "module-4.html": """
    <section class="biblio-section">
        <h2>Module 4 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Ball, S. J. (2013).</strong> <em>Foucault, Power, and Education</em>. New York: Routledge.</li>
            <li><strong>Barkley, R. A. (2015).</strong> <em>Attention-Deficit Hyperactivity Disorder: A Handbook for Diagnosis and Treatment</em> (4th ed.). New York: Guilford Press.</li>
            <li><strong>Bentham, J. (1791).</strong> <em>Panopticon: or, the Inspection-House</em>. London: T. Payne.</li>
            <li><strong>Clarke, R. (1988).</strong> 'Information Technology and Dataveillance'. <em>Communications of the ACM</em>, 31(5), 498–512.</li>
            <li><strong>Conrad, P. (1975).</strong> 'The Discovery of Hyperkinesis: Notes on the Medicalization of Deviant Behavior'. <em>Social Problems</em>, 23(1), 12–21.</li>
            <li><strong>Conrad, P. (2007).</strong> <em>The Medicalization of Society: On the Transformation of Human Conditions into Treatable Disorders</em>. Baltimore: Johns Hopkins University Press.</li>
            <li><strong>Foucault, M. (1977).</strong> <em>Discipline and Punish: The Birth of the Prison</em> (A. Sheridan, Trans.). London: Allen Lane. (Original work published in French 1975).</li>
            <li><strong>Foucault, M. (1980).</strong> <em>Power/Knowledge: Selected Interviews and Other Writings, 1972–1977</em> (C. Gordon, Ed.). New York: Pantheon Books.</li>
            <li><strong>Foucault, M. (1988).</strong> 'Technologies of the Self'. In L. H. Martin, H. Gutman, &amp; P. H. Hutton (Eds.), <em>Technologies of the Self: A Seminar with Michel Foucault</em> (pp. 16–49). Amherst: University of Massachusetts Press.</li>
            <li><strong>Foucault, M. (2008).</strong> <em>The Birth of Biopolitics: Lectures at the Collège de France, 1978–1979</em> (G. Burchell, Trans.). Basingstoke: Palgrave Macmillan.</li>
            <li><strong>Rose, N. (1999).</strong> <em>Governing the Soul: The Shaping of the Private Self</em> (2nd ed.). London: Free Association Books.</li>
            <li><strong>Rose, N. (1999).</strong> <em>Powers of Freedom: Reframing Political Thought</em>. Cambridge: Cambridge University Press.</li>
            <li><strong>Selwyn, N. (2016).</strong> <em>Is Technology Good for Education?</em> Cambridge: Polity Press.</li>
            <li><strong>Williamson, B. (2017).</strong> <em>Big Data in Education: The Digital Future of Learning, Policy and Practice</em>. London: Sage Publications.</li>
            <li><strong>Zuboff, S. (2019).</strong> <em>The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power</em>. New York: PublicAffairs.</li>
        </ul>
    </section>
""",
    "module-5.html": """
    <section class="biblio-section">
        <h2>Module 5 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Ball, S. J. (1994).</strong> <em>Education Reform: A Critical and Post-Structural Approach</em>. Buckingham: Open University Press.</li>
            <li><strong>Ball, S. J. (2003).</strong> 'The Teacher's Soul and the Terrors of Performativity'. <em>Journal of Education Policy</em>, 18(2), 215–228.</li>
            <li><strong>Chubb, J. E., &amp; Moe, T. M. (1990).</strong> <em>Politics, Markets and America's Schools</em>. Washington, D.C.: Brookings Institution Press.</li>
            <li><strong>Friedman, M. (1955).</strong> 'The Role of Government in Education'. In R. A. Solo (Ed.), <em>Economics and the Public Interest</em> (pp. 123–144). New Brunswick: Rutgers University Press.</li>
            <li><strong>Gonski, D., Boston, K., Greiner, K., Lawrence, C., Scales, B., &amp; Tannock, P. (2011).</strong> <em>Review of Funding for Schooling: Final Report</em>. Canberra: Department of Education, Employment and Workplace Relations.</li>
            <li><strong>Lingard, B. (2010).</strong> 'Policy borrowing, policy learning, and the politics of education policy: A critical review'. <em>Journal of Education Policy</em>, 25(2), 129–147.</li>
            <li><strong>Lingard, B., Martino, W., Rezai-Rashti, G., &amp; Sellar, S. (2013).</strong> 'Globalizing education policy: Treating the disease with the disease?'. <em>Globalisation, Societies and Education</em>, 11(3), 390–408.</li>
            <li><strong>Power, M. (1997).</strong> <em>The Audit Society: Rituals of Verification</em>. Oxford: Oxford University Press.</li>
            <li><strong>Sellar, S., &amp; Lingard, B. (2014).</strong> 'The OECD and the expansion of PISA: New global modes of governance in education'. <em>British Educational Research Journal</em>, 40(6), 917–936.</li>
            <li><strong>Selwyn, N. (2016).</strong> <em>Is Technology Good for Education?</em> Cambridge: Polity Press.</li>
            <li><strong>Waslander, S., Pater, C., &amp; van der Weide, M. (2010).</strong> <em>Markets in Education: An Analytical Review of Empirical Research on Market Mechanisms in Education</em>. OECD Education Working Papers, No. 52. Paris: OECD Publishing.</li>
            <li><strong>Williamson, B. (2017).</strong> <em>Big Data in Education: The Digital Future of Learning, Policy and Practice</em>. London: Sage Publications.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
            <li><strong>Zuboff, S. (2019).</strong> <em>The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power</em>. New York: PublicAffairs.</li>
        </ul>
    </section>
""",
    "module-6.html": """
    <section class="biblio-section">
        <h2>Module 6 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Cohen, S. (1972).</strong> <em>Folk Devils and Moral Panics: The Creation of the Mods and Rockers</em>. London: MacGibbon &amp; Kee.</li>
            <li><strong>Fiske, J. (1987).</strong> <em>Television Culture</em>. London: Routledge.</li>
            <li><strong>Fiske, J. (1989).</strong> <em>Reading the Popular</em>. Boston: Unwin Hyman.</li>
            <li><strong>Hall, S. (1980).</strong> 'Encoding/Decoding'. In S. Hall, D. Hobson, A. Lowe, &amp; P. Willis (Eds.), <em>Culture, Media, Language: Working Papers in Cultural Studies, 1972–79</em> (pp. 128–138). London: Hutchinson.</li>
            <li><strong>Kristeva, J. (1980).</strong> <em>Desire in Language: A Semiotic Approach to Literature and Art</em> (T. Gora, A. Jardine, &amp; L. S. Roudiez, Trans.). New York: Columbia University Press.</li>
            <li><strong>Morley, D. (1980).</strong> <em>The "Nationwide" Audience: Structure and Decoding</em>. London: British Film Institute.</li>
            <li><strong>Oliver, M. (1990).</strong> <em>The Politics of Disablement</em>. London: Macmillan.</li>
            <li><strong>Postman, N. (1985).</strong> <em>Amusing Ourselves to Death: Public Discourse in the Age of Show Business</em>. New York: Viking.</li>
            <li><strong>Postman, N. (1992).</strong> <em>Technopoly: The Surrender of Culture to Technology</em>. New York: Knopf.</li>
            <li><strong>Selwyn, N. (2016).</strong> <em>Is Technology Good for Education?</em> Cambridge: Polity Press.</li>
        </ul>
    </section>
""",
    "module-7.html": """
    <section class="biblio-section">
        <h2>Module 7 References &amp; Foundational Reading</h2>
        <ul class="biblio-list">
            <li><strong>Aristotle. (2009).</strong> <em>The Nicomachean Ethics</em> (D. Ross, Trans.; L. Brown, Ed.). Oxford: Oxford University Press.</li>
            <li><strong>Foucault, M. (1980).</strong> 'Two Lectures'. In C. Gordon (Ed.), <em>Power/Knowledge: Selected Interviews and Other Writings, 1972–1977</em> (pp. 78–108). New York: Pantheon Books.</li>
            <li><strong>Freire, P. (1970).</strong> <em>Pedagogy of the Oppressed</em> (M. B. Ramos, Trans.). New York: Herder and Herder. (Original work published in Portuguese 1968).</li>
            <li><strong>Kant, I. (1998).</strong> <em>Groundwork of the Metaphysics of Morals</em> (M. Gregor, Trans. &amp; Ed.). Cambridge: Cambridge University Press. (Original work published 1785).</li>
            <li><strong>Noddings, N. (1984).</strong> <em>Caring: A Feminine Approach to Ethics and Moral Education</em>. Berkeley: University of California Press.</li>
            <li><strong>Noddings, N. (2005).</strong> <em>The Challenge to Care in Schools: An Alternative Approach to Education</em> (2nd ed.). New York: Teachers College Press.</li>
            <li><strong>United Nations. (1989).</strong> <em>Convention on the Rights of the Child</em>. Treaty Series, 1577, 3. New York: United Nations General Assembly.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
        </ul>
    </section>
""",
}


def inject_module_bibliographies(root_dir: Path) -> None:
    for filename, bib_html in MODULE_BIBLIOGRAPHIES.items():
        file_path = root_dir / filename
        if not file_path.exists():
            print(f"Skipping {filename} (not found)")
            continue

        content = file_path.read_text(encoding="utf-8")

        # Strip any existing biblio-section inside this module
        content = re.sub(r'<section\s+class="biblio-section">.*?</section>\s*', "", content, flags=re.DOTALL)

        # Place the bibliography right above the final navigation bar or </body>
        if '<nav class="module-nav"' in content:
            # Insert right before the last module-nav bar
            parts = content.rsplit('<nav class="module-nav"', 1)
            content = f"{parts[0]}{bib_html.strip()}\n    <nav class=\"module-nav\"{parts[1]}"
        else:
            content = content.replace("</body>", f"{bib_html.strip()}\n</body>")

        file_path.write_text(content, encoding="utf-8")
        print(f"Appended dedicated bibliography to {filename}")


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
    inject_module_bibliographies(root_directory)

    commit_message = (
        "Add full bibliographies to all seven module pages\n\n"
        "Append module-specific reference sections directly before the bottom\n"
        "navigation bar on module-1.html through module-7.html, maintaining\n"
        "semantic styling and 100% citation-free markup."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
