#!/usr/bin/env python3
"""Restore all unabridged forensic dossiers from git history and regenerate

the modular revision guide with core-concepts.html as the master index portal.
"""

from pathlib import Path
import re
import subprocess
import sys

MODULE_METADATA = {
    1: {
        "title": "Module 1: Social Class & Stratification",
        "prev": None,
        "prev_lbl": "",
        "next": "module-2.html",
        "next_lbl": "Module 2",
        "overview": (
            "This module examines how modern mass education acts as an "
            "apparatus of social class reproduction rather than a neutral "
            "engine of meritocracy. Through Pierre Bourdieu's foundational "
            "concepts of cultural capital, habitus, and symbolic violence, "
            "alongside sociolinguistic codes (Basil Bernstein), working-class "
            "counter-school resistance (Paul Willis), neo-Weberian social "
            "closure, credentialism, and school residualisation, we "
            "interrogate the structural mechanisms that convert inherited "
            "class privilege into scholastic success."
        ),
    },
    2: {
        "title": "Module 2: Race, Ethnicity & Indigeneity",
        "prev": "module-1.html",
        "prev_lbl": "Module 1",
        "next": "module-3.html",
        "next_lbl": "Module 3",
        "overview": (
            "This module interrogates the racialized architectures of modern "
            "mass schooling, moving beyond surface multiculturalism to examine "
            "how education operates as a site of colonial subjugation, "
            "epistemic violence, and systemic exclusion. Drawing upon Frantz "
            "Fanon, Gayatri Spivak, David Gillborn, and Django Paris & H. "
            "Samy Alim, this module evaluates how institutional routines, "
            "curricular canons, and colorblind meritocracy preserve white "
            "majoritarian dominance while offering pathways toward "
            "culturally sustaining sovereignty."
        ),
    },
    3: {
        "title": "Module 3: Gender & Sexualities",
        "prev": "module-2.html",
        "prev_lbl": "Module 2",
        "next": "module-4.html",
        "next_lbl": "Module 4",
        "overview": (
            "This module explores how gender and sexuality are constructed, "
            "regulated, and policed within educational institutions. Moving "
            "from Raewyn Connell's structural gender regimes and hegemonic "
            "masculinity to Judith Butler's poststructuralist performativity, "
            "Adrienne Rich's compulsory heterosexuality, and Ilan Meyer's "
            "minority stress epidemiology, this module exposes the "
            "heteronormative and patriarchal hidden curriculum of schooling."
        ),
    },
    4: {
        "title": "Module 4: Governance & Subjectivity",
        "prev": "module-3.html",
        "prev_lbl": "Module 3",
        "next": "module-5.html",
        "next_lbl": "Module 5",
        "overview": (
            "Drawing primarily upon the genealogical analytics of Michel "
            "Foucault, alongside Nikolas Rose, Peter Conrad, and critical "
            "digital sociologists, this module examines how modern schooling "
            "manufactures compliance not through brute force, but through "
            "spatial architecture, temporal timetables, psychological "
            "self-audit, medicalisation, and ambient digital dataveillance."
        ),
    },
    5: {
        "title": "Module 5: Neoliberalism & Datafication",
        "prev": "module-4.html",
        "prev_lbl": "Module 4",
        "next": "module-6.html",
        "next_lbl": "Module 6",
        "overview": (
            "This module unpacks the macroeconomic transformation of public "
            "education under neoliberalism, platform capitalism, and New "
            "Public Management. Analyzing Stephen Ball's performativity, "
            "horizontal market competition, Bob Lingard's governance by "
            "numbers, and Shoshana Zuboff's surveillance capitalism, we "
            "evaluate how audit cultures, league tables, and behavioral data "
            "harvesting commodify public schooling."
        ),
    },
    6: {
        "title": "Module 6: Culture & Technology",
        "prev": "module-5.html",
        "prev_lbl": "Module 5",
        "next": "module-7.html",
        "next_lbl": "Module 7",
        "overview": (
            "This module investigates cultural production, media reception, "
            "and cognitive ecology within contemporary digital societies. "
            "Spanning Stuart Hall's active audience theory, semiotic democracy, "
            "moral panics, media ecology, and the social model of disability, "
            "we evaluate how learners negotiate, subvert, or become constrained "
            "by technological and cultural messaging."
        ),
    },
    7: {
        "title": "Module 7: Philosophy, Law & Rights",
        "prev": "module-6.html",
        "prev_lbl": "Module 6",
        "next": "bibliography.html",
        "next_lbl": "Bibliography",
        "overview": (
            "This final module synthesizes normative philosophy, legal "
            "obligations, and ethical praxis in education. Spanning Paulo "
            "Freire's critical pedagogy, relational ethics of care, common law "
            "negligence and non-delegable duties of care, UNCRC participatory "
            "rights, and Michael Young's social realism, this module prepares "
            "educators to navigate professional jurisprudence and ethical "
            "responsibility."
        ),
    },
}

MODULE_BIBLIOGRAPHIES = {
    1: """    <section class="biblio-section" id="module-references">
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
    </section>""",
    2: """    <section class="biblio-section" id="module-references">
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
    </section>""",
    3: """    <section class="biblio-section" id="module-references">
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
    </section>""",
    4: """    <section class="biblio-section" id="module-references">
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
    </section>""",
    5: """    <section class="biblio-section" id="module-references">
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
    </section>""",
    6: """    <section class="biblio-section" id="module-references">
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
    </section>""",
    7: """    <section class="biblio-section" id="module-references">
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
    </section>""",
}


def obtain_master_content(root_dir: Path) -> str:
    source_file = root_dir / "core-concepts.html"
    content = ""
    if source_file.exists():
        content = source_file.read_text(encoding="utf-8")

    # If the file on disk was overwritten with just the portal, retrieve the complete
    # monolithic file from git commit b16eae7 where every dossier is stored intact.
    if '<section id="section-2">' not in content or '<section id="section-3">' not in content:
        print("Fetching complete original document from git commit b16eae7...")
        res = subprocess.run(
            ["git", "show", "b16eae7:core-concepts.html"],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0 and '<section id="section-2">' in res.stdout:
            content = res.stdout
            print("Successfully retrieved full original document from git history.")
        else:
            print("Error: Could not retrieve full content from commit b16eae7.", file=sys.stderr)
            sys.exit(1)

    return content


def build_nav_bar(prev_url: str | None, prev_lbl: str, next_url: str | None, next_lbl: str) -> str:
    back_html = (
        f'<a href="{prev_url}" class="nav-btn">&larr; {prev_lbl}</a>'
        if prev_url
        else '<span class="nav-btn disabled">&larr; Previous</span>'
    )
    home_html = '<a href="core-concepts.html" class="nav-btn">&#8962; Home</a>'
    next_html = (
        f'<a href="{next_url}" class="nav-btn">{next_lbl} &rarr;</a>'
        if next_url
        else '<span class="nav-btn disabled">Next &rarr;</span>'
    )

    return f"""    <nav class="module-nav" aria-label="Module Navigation">
        {back_html}
        {home_html}
        {next_html}
    </nav>"""


def slugify_heading(title_text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", "", title_text)
    cleaned = re.sub(r"\(.*?\)", "", cleaned)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", cleaned.strip().lower())
    return slug.strip("-")


def build_toc(section_html: str) -> tuple[str, str]:
    toc_items = []

    def repl_h4(match: re.Match) -> str:
        full_tag = match.group(0)
        text = match.group(1).strip()
        clean_text = re.sub(r"<[^>]+>", "", text)
        slug = slugify_heading(clean_text)
        toc_items.append((slug, clean_text))
        if 'id="' not in full_tag:
            return f'<h4 class="concept-title" id="{slug}">{text}</h4>'
        return full_tag

    updated_section_html = re.sub(r'<h4 class="concept-title"[^>]*>(.*?)</h4>', repl_h4, section_html)

    if 'class="textbook-impact-box"' in updated_section_html:
        if 'id="critical-synthesis"' not in updated_section_html:
            updated_section_html = updated_section_html.replace(
                '<div class="textbook-impact-box"',
                '<div class="textbook-impact-box" id="critical-synthesis"',
                1,
            )
        toc_items.append(("critical-synthesis", "Critical Synthesis"))

    toc_items.append(("module-references", "Module References"))

    total_items = len(toc_items)
    items_markup = []
    for idx, (slug, label) in enumerate(toc_items, start=1):
        num_str = f"{idx:02d}"
        item_html = (
            f'            <li>\n'
            f'                <a href="#{slug}">\n'
            f'                    <span class="toc-index">{num_str}</span>\n'
            f'                    <span class="toc-item-label">{label}</span>\n'
            f'                </a>\n'
            f'            </li>'
        )
        items_markup.append(item_html)

    list_block = "\n".join(items_markup)

    toc_html = f"""    <!-- MODULE IN-PAGE QUICK NAVIGATION -->
    <nav class="toc-card" aria-label="Module Quick Index">
        <div class="toc-header-row">
            <h3>Quick Navigation</h3>
            <span class="toc-badge">{total_items} Entries</span>
        </div>
        <ul class="toc-grid">
{list_block}
        </ul>
    </nav>"""

    return toc_html, updated_section_html


def get_common_head(page_title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        :root {{
            --primary: #b45309;          /* Refined Warm Amber / Cognac */
            --primary-dark: #78350f;     /* Deep Russet */
            --accent-orange: #ea580c;    /* Terracotta Accent */
            --text-heading: #1c1917;     /* Warm Charcoal */
            --text-main: #292524;        /* Crisp Charcoal Body Text */
            --text-muted: #57534e;       /* Stone Muted Text */
            --bg-page: #ffffff;          /* Clean White Canvas */
            --bg-entry: #fafaf9;         /* Very Soft Warm Stone Tint */
            --bg-banner: #fffbf5;        /* Subtle Warm Paper Tint */
            --border-subtle: #e7e5e4;    /* Light Stone Border */
            --border-accent: #f59e0b;    /* Warm Amber Line Accent */
            --badge-strength-bg: #ecfdf5;
            --badge-strength-text: #047857;
            --badge-strength-border: #a7f3d0;
            --badge-audit-bg: #fff1f2;
            --badge-audit-text: #be123c;
            --badge-audit-border: #fecdd3;
            --scenario-box-bg: #f5f5f4;
            --scenario-box-border: #d6d3d1;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.65;
            max-width: 920px;
            margin: 0 auto;
            padding: 36px 20px;
            color: var(--text-main);
            background-color: var(--bg-page);
        }}
        h1, h2, h3, h4, h5 {{
            color: var(--text-heading);
            font-weight: 700;
        }}
        h1 {{
            font-size: 1.85rem;
            color: var(--primary-dark);
            border-bottom: 3px solid var(--border-accent);
            padding-bottom: 10px;
            margin-bottom: 18px;
            letter-spacing: -0.01em;
        }}
        h2 {{
            font-size: 1.25rem;
            color: var(--primary);
            margin-top: 36px;
            margin-bottom: 12px;
            border-bottom: 2px solid #fed7aa;
            padding-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        h3.tradition-header {{
            font-size: 1.05rem;
            color: var(--text-heading);
            margin-top: 24px;
            margin-bottom: 16px;
            background: #fff7ed;
            padding: 5px 12px;
            border-left: 3px solid var(--primary);
            border-radius: 0 4px 4px 0;
            font-style: normal;
        }}
        h4.concept-title {{
            font-size: 1.02rem;
            color: var(--accent-orange);
            margin-top: 0;
            margin-bottom: 6px;
            padding-top: 0;
        }}
        h5.counter-header {{
            font-size: 0.95rem;
            color: var(--primary-dark);
            margin-top: 22px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .intro-card {{
            display: flex;
            align-items: flex-start;
            gap: 18px;
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--primary);
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 24px;
        }}
        .intro-card p {{
            margin: 0;
            font-size: 0.92rem;
            color: #44403c;
            line-height: 1.6;
            text-align: justify;
        }}
        /* Lightweight Typographic Table of Contents */
        .toc-card {{
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 3px solid var(--primary);
            border-radius: 6px;
            padding: 14px 18px 16px 18px;
            margin: 20px 0 28px 0;
        }}
        .toc-header-row {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px dashed #fed7aa;
        }}
        .toc-card h3 {{
            font-size: 0.82rem;
            color: var(--primary-dark);
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
        }}
        .toc-badge {{
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .toc-grid {{
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 6px 20px;
        }}
        .toc-grid li {{
            margin: 0;
            padding: 0;
        }}
        .toc-grid a {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            padding: 3px 0;
            color: var(--text-main);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 500;
            transition: color 0.15s ease-in-out;
        }}
        .toc-index {{
            font-size: 0.74rem;
            font-weight: 700;
            color: var(--primary);
            opacity: 0.8;
            font-variant-numeric: tabular-nums;
            flex-shrink: 0;
        }}
        .toc-item-label {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .toc-grid a:hover {{
            color: var(--accent-orange);
            text-decoration: underline;
        }}
        .forensic-entry {{
            margin-bottom: 20px;
            padding: 16px 20px;
            background-color: var(--bg-entry);
            border: 1px solid var(--border-subtle);
            border-left: 3px solid #fbbf24;
            border-radius: 6px;
        }}
        .forensic-entry p {{
            margin: 0 0 8px 0;
            font-size: 0.91rem;
            text-align: justify;
        }}
        .forensic-entry ul {{
            margin: 4px 0 10px 18px;
            font-size: 0.89rem;
            line-height: 1.55;
        }}
        .forensic-entry li {{
            margin-bottom: 6px;
            text-align: justify;
        }}
        .scenario-box {{
            margin: 10px 0 14px 0;
            padding: 10px 14px;
            background-color: var(--scenario-box-bg);
            border-left: 3px solid var(--primary);
            border-radius: 0 4px 4px 0;
            font-size: 0.88rem;
            color: #334155;
        }}
        .scenario-box strong.label {{
            color: var(--primary-dark);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.03em;
            display: block;
            margin-bottom: 4px;
        }}
        .scenario-box ul {{
            margin: 4px 0 6px 16px;
        }}
        .tooltip-term {{
            position: relative;
            cursor: help;
            border-bottom: 1.5px dotted var(--primary);
            font-weight: 600;
            color: var(--primary-dark);
        }}
        .tooltip-term:hover::after,
        .tooltip-term:focus::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            width: 280px;
            padding: 8px 12px;
            background-color: #1c1917;
            color: #fefce8;
            font-size: 0.81rem;
            font-weight: 400;
            line-height: 1.45;
            border-radius: 6px;
            border: 1px solid #f59e0b;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            z-index: 100;
            white-space: normal;
            text-align: left;
        }}
        .tooltip-term:hover::before,
        .tooltip-term:focus::before {{
            content: "";
            position: absolute;
            bottom: 110%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 6px;
            border-style: solid;
            border-color: #1c1917 transparent transparent transparent;
            z-index: 100;
        }}
        .diagram-container, .counter-svg-container {{
            margin: 16px 0;
            text-align: center;
        }}
        .diagram-container svg, .counter-svg-container svg {{
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }}
        .counter-tradition-box {{
            margin-top: 18px;
            padding: 16px 18px;
            background-color: #ffffff;
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--accent-orange);
            border-radius: 6px;
        }}
        .camp-cards {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 14px;
        }}
        .camp-card {{
            background-color: #fffdfa;
            border: 1px solid #fed7aa;
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 0.86rem;
            line-height: 1.5;
        }}
        .camp-card h6 {{
            margin: 0 0 4px 0;
            color: var(--primary-dark);
            font-size: 0.88rem;
            font-weight: 700;
        }}
        .camp-card .theorist {{
            color: var(--accent-orange);
            font-weight: 600;
            font-size: 0.8rem;
            display: block;
            margin-bottom: 6px;
        }}
        .camp-card p {{
            margin: 0;
            font-size: 0.84rem;
            text-align: left;
            color: #44403c;
        }}
        .textbook-impact-box {{
            margin-bottom: 24px;
            padding: 20px 24px;
            background-color: #fffbeb;
            border: 1px solid #fde68a;
            border-left: 5px solid #d97706;
            border-radius: 6px;
            font-size: 0.92rem;
            line-height: 1.65;
        }}
        .textbook-impact-box h4.concept-title {{
            color: var(--primary-dark);
            font-size: 1.12rem;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .textbook-impact-box ul {{
            margin: 10px 0 0 20px;
        }}
        .textbook-impact-box li {{
            margin-bottom: 10px;
            text-align: justify;
        }}
        .textbook-impact-box ul ul {{
            margin-top: 6px;
        }}
        .entry-references {{
            margin-top: 14px;
            padding: 10px 14px;
            background-color: #fefce8;
            border: 1px dashed #f59e0b;
            border-radius: 4px;
            font-size: 0.84rem;
            color: #78350f;
        }}
        .entry-references strong {{
            display: block;
            color: var(--primary-dark);
            text-transform: uppercase;
            font-size: 0.76rem;
            letter-spacing: 0.04em;
            margin-bottom: 4px;
        }}
        .entry-references ul {{
            margin: 2px 0 2px 14px;
            padding-left: 0;
            line-height: 1.5;
        }}
        .entry-references li {{
            margin-bottom: 3px;
        }}
        .audit-label-critique {{
            display: inline-block;
            background-color: var(--badge-audit-bg);
            color: var(--badge-audit-text);
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 700;
            border: 1px solid var(--badge-audit-border);
        }}
        .audit-label-strength {{
            display: inline-block;
            background-color: var(--badge-strength-bg);
            color: var(--badge-strength-text);
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 700;
            border: 1px solid var(--badge-strength-border);
        }}
        .biblio-section {{
            margin-top: 48px;
            padding-top: 20px;
            border-top: 2px solid #fed7aa;
        }}
        .biblio-section h2 {{
            font-size: 1.25rem;
            color: var(--primary-dark);
            margin-top: 0;
            border-bottom: none;
            padding-bottom: 0;
        }}
        .biblio-list {{
            list-style-type: none;
            padding-left: 0;
            font-size: 0.88rem;
            line-height: 1.6;
        }}
        .biblio-list li {{
            margin-bottom: 12px;
            padding-left: 24px;
            text-indent: -24px;
        }}
        .module-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: 20px 0;
            padding: 10px 0;
            border-top: 1px solid var(--border-subtle);
            border-bottom: 1px solid var(--border-subtle);
        }}
        .nav-btn {{
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            background-color: var(--bg-banner);
            border: 1px solid var(--border-accent);
            border-radius: 6px;
            color: var(--primary-dark);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 600;
            transition: background-color 0.15s ease-in-out, color 0.15s ease-in-out;
        }}
        .nav-btn:hover {{
            background-color: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
        }}
        .nav-btn.disabled {{
            opacity: 0.4;
            pointer-events: none;
            cursor: default;
            border-color: var(--border-subtle);
        }}
        @media (max-width: 768px) {{
            .camp-cards {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
"""


def render_module(mod_num: int, raw_sec_html: str) -> str:
    meta = MODULE_METADATA[mod_num]
    head_html = get_common_head(meta["title"])
    nav_bar = build_nav_bar(meta["prev"], meta["prev_lbl"], meta["next"], meta["next_lbl"])

    # Build TOC and add semantic IDs to concept titles
    toc_html, sec_with_ids = build_toc(raw_sec_html)

    overview_box = f"""    <div class="intro-card">
        <p><strong>Module Overview:</strong> {meta["overview"]}</p>
    </div>"""

    biblio_html = MODULE_BIBLIOGRAPHIES.get(mod_num, "")

    doc_html = f"""{head_html}
{nav_bar}

{overview_box}

{toc_html}

{sec_with_ids}

{biblio_html}

{nav_bar}
</body>
</html>
"""
    return doc_html


def render_master_bibliography(raw_bib_html: str) -> str:
    head_html = get_common_head("Master Bibliography: Primary Sources & References")
    nav_bar = build_nav_bar("module-7.html", "Module 7", None, "")

    return f"""{head_html}
{nav_bar}

{raw_bib_html}

{nav_bar}
</body>
</html>
"""


def render_portal_index() -> str:
    head_html = get_common_head("Core Sociological Concepts: Exam Revision Portal")
    return f"""{head_html}
    <h1>EDCX246 Exam Revision Guide: Forensic Concept Analysis</h1>

    <div class="intro-card">
        <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Forensic Dossier Icon" style="flex-shrink: 0; width: 72px; height: 72px;">
            <path d="M14 26C14 22.6863 16.6863 20 20 20H44L52 30H100C103.314 30 106 32.6863 106 36V90C106 93.3137 103.314 96 100 96H20C16.6863 96 14 93.3137 14 90V26Z" fill="#D97706"/>
            <rect x="25" y="22" width="70" height="68" rx="3" fill="#F5F5F4" stroke="#D6D3D1" stroke-width="1.2"/>
            <rect x="29" y="15" width="70" height="75" rx="3" fill="#FFFFFF" stroke="#A8A29E" stroke-width="1.2"/>
            <line x1="38" y1="27" x2="65" y2="27" stroke="#B45309" stroke-width="2.5" stroke-linecap="round"/>
            <line x1="38" y1="35" x2="88" y2="35" stroke="#78716C" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="38" y1="41" x2="84" y2="41" stroke="#A8A29E" stroke-width="1.3" stroke-linecap="round"/>
            <line x1="38" y1="47" x2="76" y2="47" stroke="#A8A29E" stroke-width="1.3" stroke-linecap="round"/>
            <rect x="58" y="55" width="34" height="15" rx="2" fill="#FFF1F2" stroke="#BE123C" stroke-width="1.2"/>
            <text x="61" y="66" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" font-weight="700" fill="#BE123C" letter-spacing="0.8">AUDIT</text>
            <path d="M12 44C12 40.6863 14.6863 38 18 38H102C105.314 38 108 40.6863 108 44L103 94C103 97.3137 100.314 100 97 100H23C19.6863 100 17 97.3137 17 94L12 44Z" fill="#B45309"/>
            <circle cx="60" cy="52" r="4.5" fill="#FEF3C7" stroke="#78350F" stroke-width="1.5"/>
            <line x1="60" y1="48" x2="60" y2="56" stroke="#78350F" stroke-width="1.5"/>
            <circle cx="86" cy="80" r="13" fill="#FFFFFF" fill-opacity="0.25" stroke="#44403C" stroke-width="2.5"/>
            <circle cx="86" cy="80" r="11" stroke="#F59E0B" stroke-width="1.2" stroke-dasharray="2 2"/>
            <line x1="95" y1="89" x2="106" y2="100" stroke="#44403C" stroke-width="4" stroke-linecap="round"/>
        </svg>
        <div>
            <p style="margin: 0 0 10px 0; font-size: 0.94rem; color: #44403c; line-height: 1.65; text-align: justify;">
                Welcome to the official exam revision portal for <strong>EDCX246 (Sociology of Education)</strong>, designed around
                <em>Making Sense of Mass Education</em> (4th Edition). This resource applies an uncompromising
                <strong>four-part forensic audit</strong> to core sociological theories: unpacking historical genesis and empirical anomalies,
                internal theoretical mechanisms, legitimate diagnostic strengths, and rigorous critical blind spots.
            </p>
            <p style="margin: 0; font-size: 0.94rem; color: #44403c; line-height: 1.65; text-align: justify;">
                Select a thematic module below to enter the modular study dossiers, complete with interactive popover definitions,
                concrete classroom scenario models, and inline architectural SVG flow diagrams.
            </p>
        </div>
    </div>

    <h2>Examination Revision Modules</h2>

    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 40px;">
        <a href="module-1.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">1. Social Class &amp; Stratification</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Examines cultural capital, habitus, symbolic violence, sociolinguistic codes, counter-school resistance, social closure, credentialism, and residualisation.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 1 &rarr;</span>
        </a>

        <a href="module-2.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">2. Race, Ethnicity &amp; Indigeneity</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Investigates colonial psychology, epistemic violence, institutional racism, whiteness as policy, and culturally sustaining pedagogies.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 2 &rarr;</span>
        </a>

        <a href="module-3.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">3. Gender &amp; Sexualities</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Analyzes institutional gender regimes, hegemonic masculinity, gender performativity, compulsory heterosexuality, and minority stress models.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 3 &rarr;</span>
        </a>

        <a href="module-4.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">4. Governance &amp; Subjectivity</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Deconstructs Foucaultian disciplinary power, panopticism, governmentality, technologies of the self, the psy-complex, and digital dataveillance.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 4 &rarr;</span>
        </a>

        <a href="module-5.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">5. Neoliberalism &amp; Datafication</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Evaluates performativity, audit cultures, horizontal market competition, governance by numbers, accountability washback, and surveillance capitalism.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 5 &rarr;</span>
        </a>

        <a href="module-6.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">6. Culture &amp; Technology</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Explores active audience theory, polysemy, semiotic democracy, moral panics, media ecology, and the social model of disability.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 6 &rarr;</span>
        </a>

        <a href="module-7.html" style="background-color: var(--bg-entry); border: 1px solid var(--border-subtle); border-left: 4px solid var(--accent-orange); border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: var(--primary-dark); margin-top: 0; margin-bottom: 8px;">7. Philosophy, Law &amp; Rights</h3>
            <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; text-align: justify;">Synthesizes critical pedagogy, normative ethics, non-delegable duty of care, UNCRC participatory rights, and powerful knowledge frameworks.</p>
            <span style="margin-top: 12px; font-size: 0.85rem; font-weight: 700; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 0.03em;">Open Module 7 &rarr;</span>
        </a>

        <a href="bibliography.html" style="grid-column: span 2; background-color: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #d97706; border-radius: 6px; padding: 18px 20px; text-decoration: none; display: flex; flex-direction: column;">
            <h3 style="font-size: 1.05rem; color: #78350f; margin-top: 0; margin-bottom: 8px;">Master Bibliography &amp; References</h3>
            <p style="margin: 0; font-size: 0.88rem; color: #78350f; line-height: 1.5; text-align: justify;">Comprehensive, alphabetized catalogue of all primary sociological texts, empirical studies, and critical counter-texts referenced across the revision modules.</p>
            <span style="margin-top: 10px; font-size: 0.85rem; font-weight: 700; color: #d97706; text-transform: uppercase; letter-spacing: 0.03em; display: inline-block;">Open Master Bibliography &rarr;</span>
        </a>
    </div>

</body>
</html>
"""


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
    master_html = obtain_master_content(root_directory)

    # 1. Generate individual module files by cleanly slicing from master_html
    for i in range(1, 8):
        pattern = rf'(<section id="section-{i}"\s*>.*?</section>)'
        match = re.search(pattern, master_html, re.DOTALL)
        if not match:
            print(f"Warning: Could not find section-{i} in master content!", file=sys.stderr)
            continue

        raw_sec = match.group(1)
        mod_page_content = render_module(i, raw_sec)
        out_file = root_directory / f"module-{i}.html"
        out_file.write_text(mod_page_content, encoding="utf-8")
        print(f"Restored full content in: {out_file.name}")

    # 2. Extract and generate master bibliography
    bib_match = re.search(r'(<section id="master-bibliography".*?</section>)', master_html, re.DOTALL)
    if bib_match:
        raw_bib = bib_match.group(1)
        bib_doc = render_master_bibliography(raw_bib)
        bib_file = root_directory / "bibliography.html"
        bib_file.write_text(bib_doc, encoding="utf-8")
        print(f"Restored: {bib_file.name}")

    # 3. Generate master index portal
    index_file = root_directory / "core-concepts.html"
    index_file.write_text(render_portal_index(), encoding="utf-8")
    print(f"Generated index portal: {index_file.name}")

    commit_message = (
        "Restore full dossiers and modularize revision guide from git history\n\n"
        "Recover complete, unabridged sociological dossiers from git commit\n"
        "b16eae7 and distribute them across dedicated module pages (module-1.html\n"
        "to module-7.html) with core-concepts.html as the primary landing portal.\n\n"
        "- Extract complete theoretical dossiers, scenarios, SVGs, and audits.\n"
        "- Inject linear navigation controls (Previous, Home, Next) on all pages.\n"
        "- Add module overview cards and in-page quick navigation directories.\n"
        "- Append dedicated reference lists to modules 1 through 7.\n"
        "- Rebuild core-concepts.html as the master index portal.\n"
        "- Maintain 100% citation-free markup across all HTML files."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
