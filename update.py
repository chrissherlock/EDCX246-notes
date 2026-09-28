#!/usr/bin/env python3
"""Regenerate core-concepts.html and all modular section pages with rich

introductory cards, maintaining clean citation-free markup and automated git
synchronization.
"""

from pathlib import Path
import subprocess
import sys


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
            background-color: #f5f5f4;
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
            background-color: #fff1f2;
            color: #be123c;
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 700;
            border: 1px solid #fecdd3;
        }}
        .audit-label-strength {{
            display: inline-block;
            background-color: #ecfdf5;
            color: #047857;
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 700;
            border: 1px solid #a7f3d0;
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
        .back-link {{
            display: inline-block;
            margin-top: 28px;
            margin-bottom: 24px;
            padding: 7px 14px;
            background-color: #fff7ed;
            border: 1px solid #fdba74;
            border-radius: 5px;
            color: var(--primary-dark);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 600;
            transition: all 0.15s ease-in-out;
        }}
        .back-link:hover {{
            background-color: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
        }}
        @media (max-width: 768px) {{
            .camp-cards {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
"""


def generate_core_concepts_index_html() -> str:
    return f"""{get_common_head("Core Sociological Concepts: Exam Revision Portal")}
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


def generate_module_1_html() -> str:
    return f"""{get_common_head("Module 1: Social Class & Stratification")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-1">
        <h2>1. Social Class &amp; Educational Stratification</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> This module examines how modern mass education acts as an apparatus of social class reproduction rather than a neutral engine of meritocracy. Through Pierre Bourdieu's foundational concepts of <em>cultural capital</em> and <em>habitus</em>, alongside sociolinguistic codes (Basil Bernstein), working-class resistance (Paul Willis), neo-Weberian social closure, credentialism, and school residualisation, we interrogate the structural mechanisms that convert inherited class privilege into academic success.
            </p>
        </div>

        <h3 class="tradition-header">The Bourdieusian Paradigm (Pierre Bourdieu &amp; Jean-Claude Passeron)</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Cultural Capital (Pierre Bourdieu)</h4>
            <p>Cultural capital represents the accumulated, embodied labor-time invested in non-financial social assets—syntactic fluency, academic mannerisms, aesthetic dispositions, and formal credentials—that individuals inherit through domestic class socialization and deploy within competitive institutional markets. Rather than reflecting neutral, biological intelligence, it operates as an institutionalized class currency that schools covertly demand and reward while pretending merely to evaluate innate merit.</p>

            <div class="scenario-box">
                <strong class="label">Concrete Mechanism in Action: Julian vs. Marcus</strong>
                Imagine two 10-year-olds with identical raw working memory and cognitive aptitude:
                <ul>
                    <li><strong>Julian (Solicitor &amp; Teacher household):</strong> Absorbs thousands of hours of speculative debate, sophisticated vocabulary (<em>"tentatively"</em>, <em>"contradictory"</em>), and museum visits through domestic osmosis. He instinctively knows how to challenge authority politely, make eye contact, and structure arguments in an essay.</li>
                    <li><strong>Marcus (Forklift driver &amp; Cleaner household):</strong> Absorbs practical problem-solving, trade knowledge, community solidarity, and direct, protective language (<em>"hurry up"</em>, <em>"don't get into trouble"</em>).</li>
                </ul>
                When the school tests <em>"authoritative voice,"</em> <em>"nuanced engagement,"</em> and <em>"formal rhetoric,"</em> it rewards Julian for speaking his home dialect while penalizing Marcus for lacking a code the school never explicitly taught him. The school acts like a foreign currency exchange that demands US Dollars, takes payment from the child raised in America, and penalizes the child holding Pesos—all while claiming to be an objective, meritocratic test.
            </div>

            <!-- THE CRITICAL COUNTER-TRADITION & SVG DIAGRAM -->
            <div class="counter-tradition-box">
                <h5 class="counter-header">The Critical Counter-Tradition: Three Camps of Resistance</h5>
                <p>
                    Sociological textbooks frequently present Bourdieu's reproduction thesis as an uncontested terminal diagnosis.
                    In reality, an authoritative counter-tradition of educational realists, sociologists, and philosophers exposes
                    fatal blind spots in his framework across three distinct vectors of attack:
                </p>

                <div class="counter-svg-container">
                    <svg viewBox="0 0 760 260" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="The Three Counter-Argument Camps">
                        <rect x="10" y="10" width="740" height="240" rx="8" fill="#FFFDF8" stroke="#FED7AA" stroke-width="1.5"/>
                        <rect x="250" y="25" width="260" height="52" rx="6" fill="#78350F" stroke="#451A03" stroke-width="1.5"/>
                        <text x="380" y="47" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11.5" font-weight="800" fill="#FEF3C7" text-anchor="middle">BOURDIEU'S REPRODUCTION THESIS</text>
                        <text x="380" y="63" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" fill="#FDE68A" text-anchor="middle">Schooling as Closed Symbolic Violence &amp; Arbitrary Sorting</text>
                        <path d="M310 77 V 110 H 135 V 130" stroke="#B45309" stroke-width="2" stroke-dasharray="3 3"/>
                        <path d="M380 77 V 130" stroke="#B45309" stroke-width="2"/>
                        <path d="M450 77 V 110 H 625 V 130" stroke="#B45309" stroke-width="2" stroke-dasharray="3 3"/>
                        <polygon points="135,135 131,125 139,125" fill="#B45309"/>
                        <polygon points="380,135 376,125 384,125" fill="#B45309"/>
                        <polygon points="625,135 621,125 629,125" fill="#B45309"/>
                        <rect x="25" y="136" width="220" height="98" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                        <rect x="25" y="136" width="220" height="24" rx="6" fill="#FEF3C7"/>
                        <text x="135" y="152" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="800" fill="#78350F" text-anchor="middle">1. THE EPISTEMIC CRITIQUE</text>
                        <text x="135" y="174" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="700" fill="#EA580C" text-anchor="middle">Michael Young (Social Realism)</text>
                        <text x="135" y="193" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#44403C" text-anchor="middle">Powerful Knowledge vs. Power's Knowledge</text>
                        <text x="135" y="209" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Curriculum is not arbitrary etiquette;</text>
                        <text x="135" y="221" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">it is testable, objective intellectual power.</text>
                        <rect x="270" y="136" width="220" height="98" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                        <rect x="270" y="136" width="220" height="24" rx="6" fill="#FEF3C7"/>
                        <text x="380" y="152" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="800" fill="#78350F" text-anchor="middle">2. PEDAGOGICAL REALISM</text>
                        <text x="380" y="174" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="700" fill="#EA580C" text-anchor="middle">Lisa Delpit (The Culture of Power)</text>
                        <text x="380" y="193" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#44403C" text-anchor="middle">Explicit Teaching vs. Progressive Sabotage</text>
                        <text x="380" y="209" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Hiding the rules strands poor kids;</text>
                        <text x="380" y="221" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">equity demands teaching codes explicitly.</text>
                        <rect x="515" y="136" width="220" height="98" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                        <rect x="515" y="136" width="220" height="24" rx="6" fill="#FEF3C7"/>
                        <text x="625" y="152" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="800" fill="#78350F" text-anchor="middle">3. PHILOSOPHICAL AGENCY</text>
                        <text x="625" y="174" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="700" fill="#EA580C" text-anchor="middle">Jacques Rancière (The Master's Trap)</text>
                        <text x="625" y="193" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#44403C" text-anchor="middle">Intellectual Equality vs. Sociological Paternalism</text>
                        <text x="625" y="209" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">The poor are not unthinking cultural dupes;</text>
                        <text x="625" y="221" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">they see through institutional hypocrisy clearly.</text>
                    </svg>
                </div>
            </div>
        </div>

        <div class="textbook-impact-box">
            <h4 class="concept-title">Critical Synthesis: Impact on <em>Making Sense of Mass Education</em> (The Bourdieusian Paradigm)</h4>
            <p>
                Bourdieu's reproduction model within the textbook is <strong>indispensable as an anatomical X-ray of inherited privilege, but toxic as a standalone pedagogical compass</strong>.
            </p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_module_2_html() -> str:
    return f"""{get_common_head("Module 2: Race, Ethnicity & Indigeneity")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-2">
        <h2>2. Race, Ethnicity &amp; Indigeneity</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> This module interrogates the racialized architectures of modern mass education, moving beyond surface multiculturalism to examine how schools operate as sites of colonial subjugation, epistemic violence, and systemic exclusion. Drawing upon Frantz Fanon, Gayatri Spivak, David Gillborn, and Django Paris &amp; H. Samy Alim, this module evaluates how institutional routines, curricular canons, and colorblind meritocracy preserve white majoritarian dominance while offering pathways toward culturally sustaining sovereignty.
            </p>
        </div>

        <h3 class="tradition-header">Postcolonial &amp; Critical Race Paradigms</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Colonisation of the Mind (Frantz Fanon)</h4>
            <p>Frantz Fanon's psychoanalytic and anti-colonial framework demonstrates that colonial subjugation operates through the psychic colonization of the colonized subject's interiority.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Epistemic Violence (Gayatri Spivak)</h4>
            <p>Spivak's postcolonial thesis demonstrates the institutional silencing, delegitimation, and destruction of non-Western knowledge traditions by dominant colonial epistemologies.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Institutional Racism &amp; Whiteness as Policy (David Gillborn)</h4>
            <p>Examines how ostensibly race-neutral routines and curriculum standards operate as whiteness as policy, engineering racial inequality under colorblind meritocracy.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Culturally Sustaining Pedagogy (Django Paris &amp; H. Samy Alim)</h4>
            <p>Requires schools to actively perpetuate, sustain, and revitalize linguistic and cultural traditions of marginalized communities as sovereign intellectual heritage.</p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_module_3_html() -> str:
    return f"""{get_common_head("Module 3: Gender & Sexualities")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-3">
        <h2>3. Gender &amp; Sexualities</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> This module explores how gender and sexuality are constructed, regulated, and policed within educational institutions. Moving from Raewyn Connell's structural gender regimes and hegemonic masculinity to Judith Butler's poststructuralist performativity, Adrienne Rich's compulsory heterosexuality, and Ilan Meyer's minority stress epidemiology, this module exposes the heteronormative and patriarchal hidden curriculum of schooling.
            </p>
        </div>

        <h3 class="tradition-header">Structural Gender Orders &amp; Poststructuralist Performativity</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Gender Regimes &amp; Hegemonic Masculinity (Raewyn Connell)</h4>
            <p>Connell's sociology posits that gender is an evolving historical structure of power, labor, emotional investment, and symbolism structured around hegemonic masculinity.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Gender Performativity (Judith Butler)</h4>
            <p>Butler's poststructuralist thesis demonstrates that gender is performative: an ongoing repetition of bodily gestures and speech acts that produces the illusion of an innate core.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Compulsory Heterosexuality (Adrienne Rich)</h4>
            <p>Rich's radical feminist critique demonstrates that heterosexuality is an institutionalized political apparatus engineered to enforce social conformity and male dominance.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Minority Stress &amp; Affirmative Pedagogy (Ilan Meyer)</h4>
            <p>Establishes that psychological distress among LGBTQ+ students is the chronic psychological toll of enduring hostile, invalidating institutional environments.</p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_module_4_html() -> str:
    return f"""{get_common_head("Module 4: Governance & Subjectivity")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-4">
        <h2>4. Governance, Surveillance &amp; Subjectivity</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> Drawing primarily upon the genealogical analytics of Michel Foucault, alongside Nikolas Rose, Peter Conrad, and digital sociologists, this module examines how modern schooling manufactures compliance not through brute force, but through spatial architecture, temporal timetables, psychological self-audit, medicalisation, and ambient digital dataveillance.
            </p>
        </div>

        <h3 class="tradition-header">The Foucaultian Architecture of Power</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Disciplinary Power &amp; Docile Bodies (Michel Foucault)</h4>
            <p>Foucault's genealogy demonstrates how modern institutions train and coordinate human bodies through spatial distribution and temporal scheduling to manufacture docile bodies.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">The Panopticon &amp; The Disciplinary Triad (Michel Foucault)</h4>
            <p>Describes how permanent visibility and the Disciplinary Triad transform human subjects into self-regulating, quantifiable entities.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Governmentality &amp; Technologies of the Self (Michel Foucault)</h4>
            <p>The art of governing at a distance, where autonomous individuals voluntarily deploy self-auditing and reflection to align with institutional objectives.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">The Psy-Complex &amp; Medicalisation of Deviance (Nikolas Rose / Peter Conrad)</h4>
            <p>Reveals how modern schooling systematically redefines behavioral non-compliance as organic psychiatric pathologies through the psy-complex.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Digital Panopticon &amp; Dataveillance</h4>
            <p>The ubiquitous algorithmic monitoring of student cognitive and physical presence across school and domestic environments through LMS telemetry.</p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_module_5_html() -> str:
    return f"""{get_common_head("Module 5: Neoliberalism & Datafication")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-5">
        <h2>5. Neoliberalism &amp; Datafication</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> This module unpacks the macro-economic transformation of public education under neoliberalism, platform capitalism, and New Public Management. Analyzing Stephen Ball's performativity, horizontal market competition, Bob Lingard's governance by numbers, and Shoshana Zuboff's surveillance capitalism, we evaluate how audit cultures, league tables, and behavioral data harvesting commodify public schooling.
            </p>
        </div>

        <h3 class="tradition-header">Marketization, Managerialism &amp; Platform Capitalism</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Performativity &amp; Audit Culture (Stephen Ball)</h4>
            <p>Ball's critique demonstrates that modern educational governance replaces professional autonomy with quantifiable performance indicators and audit cultures.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Horizontal Competition</h4>
            <p>Describes zero-sum market contests between schools competing through cream-skimming, glossy branding, and exclusionary intake curation.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Governance by Numbers &amp; Accountability Washback (Bob Lingard)</h4>
            <p>Lingard's framework describing how centralized census testing steers education systems remotely through governance by numbers, producing severe accountability washback.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Surveillance Capitalism (Shoshana Zuboff)</h4>
            <p>Zuboff's framework describing how commercial tech monopolies claim private human experience as behavioral surplus for predictive modification and profit.</p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_module_6_html() -> str:
    return f"""{get_common_head("Module 6: Culture & Technology")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-6">
        <h2>6. Culture &amp; Technology</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> This module investigates cultural production, media reception, and cognitive ecology within contemporary digital societies. Spanning Stuart Hall's active audience theory, semiotic democracy, moral panics, media ecology, and the social model of disability, we evaluate how learners negotiate, subvert, or become constrained by technological and cultural messaging.
            </p>
        </div>

        <h3 class="tradition-header">Media Studies, Subcultural Agency &amp; Cognitive Ecology</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Active Audience Theory &amp; Polysemy (Stuart Hall)</h4>
            <p>Hall's encoding/decoding model demonstrating that media texts are polysemic (bearing multiple interpretations) and actively negotiated by audiences through dominant, negotiated, or oppositional stances.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Semiotic Democracy &amp; Textual Poaching (John Fiske)</h4>
            <p>Youth audiences actively seize corporate cultural products, remixing and subverting corporate signs to construct autonomous meaning.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Intertextuality &amp; Moral Panics (Julia Kristeva / Stanley Cohen)</h4>
            <p>Examines media-manufactured societal panics framing youth behaviors or educational standards as existential threats.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Media Ecology &amp; The Social Model of Disability (Neil Postman / Mike Oliver)</h4>
            <p>Postman's analysis of technological trade-offs paired with Oliver's social model defining disability as an institutional mismatch with inaccessible environments.</p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_module_7_html() -> str:
    return f"""{get_common_head("Module 7: Philosophy, Law & Rights")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="section-7">
        <h2>7. Philosophy, Law &amp; Educational Rights</h2>

        <div class="intro-card">
            <p>
                <strong>Module Overview:</strong> This final module synthesizes normative philosophy, legal obligations, and ethical praxis in education. Spanning Paulo Freire's critical pedagogy, relational ethics of care, common law negligence and non-delegable duties of care, UNCRC participatory rights, and Michael Young's social realism, this module prepares educators to navigate professional jurisprudence and ethical responsibility.
            </p>
        </div>

        <h3 class="tradition-header">Critical Praxis, Ethics &amp; Jurisprudence</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Critical Pedagogy &amp; Praxis (Paulo Freire)</h4>
            <p>Freire's critique of the banking model of education in favor of problem-posing dialogue, conscientisation, and praxis.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Normative Ethics &amp; Relational Care (Nel Noddings / Aristotle)</h4>
            <p>Philosophical synthesis of Kantian deontology, Aristotelian phronesis, and Nel Noddings' ethics of care.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Non-Delegable Duty of Care &amp; Negligence</h4>
            <p>Common law tort doctrine imposing an affirmative duty upon schools and teachers to take reasonable precautions against foreseeable harm.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">UNCRC Article 12 &amp; Participatory Rights</h4>
            <p>Guarantees children the right to express their views freely in all matters affecting them, disrupting institutional paternalism.</p>
        </div>
        <div class="forensic-entry">
            <h4 class="concept-title">Regimes of Truth vs. Powerful Knowledge (Michel Foucault / Michael Young)</h4>
            <p>Intellectual tension between Foucault's poststructuralist critique of truth regimes and Young's Social Realism defending universal access to powerful knowledge.</p>
        </div>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
</body>
</html>
"""


def generate_bibliography_html() -> str:
    return f"""{get_common_head("Master Bibliography: Primary Sources & References")}
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
    <section id="master-bibliography" class="biblio-section">
        <h2>Master Bibliography: Primary Sources &amp; Critical References</h2>
        <ul class="biblio-list">
            <li><strong>Achebe, C. (1975).</strong> <em>Morning Yet on Creation Day: Essays</em>. London: Heinemann.</li>
            <li><strong>Ball, S. J. (1994).</strong> <em>Education Reform: A Critical and Post-Structural Approach</em>. Buckingham: Open University Press.</li>
            <li><strong>Ball, S. J. (2003).</strong> 'The Teacher's Soul and the Terrors of Performativity'. <em>Journal of Education Policy</em>, 18(2), 215–228.</li>
            <li><strong>Ball, S. J. (2013).</strong> <em>Foucault, Power, and Education</em>. New York: Routledge.</li>
            <li><strong>Barkley, R. A. (2015).</strong> <em>Attention-Deficit Hyperactivity Disorder: A Handbook for Diagnosis and Treatment</em> (4th ed.). New York: Guilford Press.</li>
            <li><strong>Bell, D. A. (1980).</strong> 'Brown v. Board of Education and the Interest-Convergence Dilemma'. <em>Harvard Law Review</em>, 93(3), 518–533.</li>
            <li><strong>Bentham, J. (1791).</strong> <em>Panopticon: or, the Inspection-House</em>. London: T. Payne.</li>
            <li><strong>Bernstein, B. (1971).</strong> <em>Class, Codes and Control: Volume 1, Theoretical Studies Towards a Sociology of Language</em>. London: Routledge &amp; Kegan Paul.</li>
            <li><strong>Bourdieu, P. (1973).</strong> 'Cultural Reproduction and Social Reproduction'. In R. Brown (Ed.), <em>Knowledge, Education, and Cultural Change: Papers in the Sociology of Education</em> (pp. 71–112). London: Tavistock Publications.</li>
            <li><strong>Bourdieu, P. (1977).</strong> <em>Outline of a Theory of Practice</em> (R. Nice, Trans.). Cambridge: Cambridge University Press. (Original work published in French 1972).</li>
            <li><strong>Bourdieu, P. (1984).</strong> <em>Distinction: A Social Critique of the Judgement of Taste</em> (R. Nice, Trans.). Cambridge, MA: Harvard University Press. (Original work published in French 1979).</li>
            <li><strong>Bourdieu, P. (1986).</strong> 'The Forms of Capital'. In J. G. Richardson (Ed.), <em>Handbook of Theory and Research for the Sociology of Education</em> (pp. 241–258). New York: Greenwood Press.</li>
            <li><strong>Bourdieu, P., &amp; Passeron, J.-C. (1977).</strong> <em>Reproduction in Education, Society and Culture</em> (R. Nice, Trans.). London: Sage Publications. (Original work published in French 1970).</li>
            <li><strong>Butler, J. (1990).</strong> <em>Gender Trouble: Feminism and the Subversion of Identity</em>. New York: Routledge.</li>
            <li><strong>Butler, J. (1993).</strong> <em>Bodies That Matter: On the Discursive Limits of "Sex"</em>. New York: Routledge.</li>
            <li><strong>Chubb, J. E., &amp; Moe, T. M. (1990).</strong> <em>Politics, Markets and America's Schools</em>. Washington, D.C.: Brookings Institution Press.</li>
            <li><strong>Clarke, R. (1988).</strong> 'Information Technology and Dataveillance'. <em>Communications of the ACM</em>, 31(5), 498–512.</li>
            <li><strong>Collins, R. (1979).</strong> <em>The Credential Society: An Historical Sociology of Education and Stratification</em>. New York: Academic Press.</li>
            <li><strong>Connell, R. W. (1987).</strong> <em>Gender and Power: Society, the Person and Sexual Politics</em>. Stanford: Stanford University Press.</li>
            <li><strong>Connell, R. W. (1995).</strong> <em>Masculinities</em>. Berkeley: University of California Press.</li>
            <li><strong>Conrad, P. (2007).</strong> <em>The Medicalization of Society: On the Transformation of Human Conditions into Treatable Disorders</em>. Baltimore: Johns Hopkins University Press.</li>
            <li><strong>Delpit, L. (1988).</strong> 'The Silenced Dialogue: Power and Pedagogy in Educating Other People's Children'. <em>Harvard Educational Review</em>, 58(3), 280–298.</li>
            <li><strong>Delpit, L. (1995).</strong> <em>Other People's Children: Cultural Conflict in the Classroom</em>. New York: The New Press.</li>
            <li><strong>Fanon, F. (1967).</strong> <em>Black Skin, White Masks</em> (C. L. Markmann, Trans.). New York: Grove Press. (Original work published in French 1952).</li>
            <li><strong>Fanon, F. (1963).</strong> <em>The Wretched of the Earth</em> (C. Farrington, Trans.). New York: Grove Press. (Original work published in French 1961).</li>
            <li><strong>Foucault, M. (1977).</strong> <em>Discipline and Punish: The Birth of the Prison</em> (A. Sheridan, Trans.). London: Allen Lane. (Original work published in French 1975).</li>
            <li><strong>Foucault, M. (1988).</strong> 'Technologies of the Self'. In L. H. Martin, H. Gutman, &amp; P. H. Hutton (Eds.), <em>Technologies of the Self: A Seminar with Michel Foucault</em> (pp. 16–49). Amherst: University of Massachusetts Press.</li>
            <li><strong>Foucault, M. (2008).</strong> <em>The Birth of Biopolitics: Lectures at the Collège de France, 1978–1979</em> (G. Burchell, Trans.). Basingstoke: Palgrave Macmillan.</li>
            <li><strong>Freire, P. (1970).</strong> <em>Pedagogy of the Oppressed</em> (M. B. Ramos, Trans.). New York: Herder and Herder. (Original work published in Portuguese 1968).</li>
            <li><strong>Friedman, M. (1955).</strong> 'The Role of Government in Education'. In R. A. Solo (Ed.), <em>Economics and the Public Interest</em> (pp. 123–144). New Brunswick: Rutgers University Press.</li>
            <li><strong>Fricker, M. (2007).</strong> <em>Epistemic Injustice: Power and the Ethics of Knowing</em>. Oxford: Oxford University Press.</li>
            <li><strong>Gillborn, D. (2005).</strong> 'Education policy as an act of white supremacy: Whiteness, critical race theory and education reform'. <em>Journal of Education Policy</em>, 20(4), 485–505.</li>
            <li><strong>Gillborn, D. (2008).</strong> <em>Racism and Education: Coincidence or Conspiracy?</em> London: Routledge.</li>
            <li><strong>Gonski, D., Boston, K., Greiner, K., Lawrence, C., Scales, B., &amp; Tannock, P. (2011).</strong> <em>Review of Funding for Schooling: Final Report</em>. Canberra: Department of Education, Employment and Workplace Relations.</li>
            <li><strong>Hall, S. (1980).</strong> 'Encoding/Decoding'. In S. Hall, D. Hobson, A. Lowe, &amp; P. Willis (Eds.), <em>Culture, Media, Language: Working Papers in Cultural Studies, 1972–79</em> (pp. 128–138). London: Hutchinson.</li>
            <li><strong>Kosciw, J. G., Clark, C. M., Truong, N. L., &amp; Zongrone, A. D. (2020).</strong> <em>The 2019 National School Climate Survey: The Experiences of Lesbian, Gay, Bisexual, Transgender, and Queer Youth in Our Nation's Schools</em>. New York: GLSEN.</li>
            <li><strong>Labov, W. (1972).</strong> <em>Language in the Inner City: Studies in the Black English Vernacular</em>. University of Pennsylvania Press.</li>
            <li><strong>Ladson-Billings, G. (1995).</strong> 'Toward a Theory of Culturally Relevant Pedagogy'. <em>American Educational Research Journal</em>, 32(3), 465–491.</li>
            <li><strong>Lingard, B. (2010).</strong> 'Policy borrowing, policy learning, and the politics of education policy: A critical review'. <em>Journal of Education Policy</em>, 25(2), 129–147.</li>
            <li><strong>Lingard, B., Martino, W., Rezai-Rashti, G., &amp; Sellar, S. (2013).</strong> 'Globalizing education policy: Treating the disease with the disease?'. <em>Globalisation, Societies and Education</em>, 11(3), 390–408.</li>
            <li><strong>Macaulay, T. B. (1835).</strong> <em>Minute on Indian Education</em>. London: British Parliamentary Papers.</li>
            <li><strong>Macpherson, W. (1999).</strong> <em>The Stephen Lawrence Inquiry: Report of an Inquiry by Sir William Macpherson of Cluny</em>. London: The Stationery Office.</li>
            <li><strong>Mayo, C. (2014).</strong> <em>LGBTQ Youth and Education: Policies and Practices</em>. New York: Teachers College Press.</li>
            <li><strong>Meyer, I. H. (2003).</strong> 'Prejudice, Social Stress, and Mental Health in Lesbian, Gay, and Bisexual Populations: Conceptual Issues and Research Evidence'. <em>Psychological Bulletin</em>, 129(5), 674–697.</li>
            <li><strong>Ngũgĩ wa Thiong'o. (1986).</strong> <em>Decolonising the Mind: The Politics of Language in African Literature</em>. London: James Currey.</li>
            <li><strong>Nussbaum, M. (1999).</strong> 'The Professor of Parody: The Hip Defeatism of Judith Butler'. <em>The New Republic</em>, 220(8), 37–45.</li>
            <li><strong>Paris, D. (2012).</strong> 'Culturally Sustaining Pedagogy: A Needed Change in Stance, Terminology, and Practice'. <em>Educational Researcher</em>, 41(3), 93–97.</li>
            <li><strong>Paris, D., &amp; Alim, H. S. (Eds.). (2017).</strong> <em>Culturally Sustaining Pedagogies: Teaching and Learning for Justice in a Changing World</em>. New York: Teachers College Press.</li>
            <li><strong>Power, M. (1997).</strong> <em>The Audit Society: Rituals of Verification</em>. Oxford: Oxford University Press.</li>
            <li><strong>Rancière, J. (2004).</strong> <i>The Philosopher and His Poor</i> (J. Drury, C. Oster, &amp; A. Parker, Trans.). Durham, NC: Duke University Press.</li>
            <li><strong>Rich, A. (1980).</strong> 'Compulsory Heterosexuality and Lesbian Existence'. <em>Signs: Journal of Women in Culture and Society</em>, 5(4), 631–660.</li>
            <li><strong>Rose, N. (1999).</strong> <em>Governing the Soul: The Shaping of the Private Self</em> (2nd ed.). London: Free Association Books.</li>
            <li><strong>Sellar, S., &amp; Lingard, B. (2014).</strong> 'The OECD and the expansion of PISA: New global modes of governance in education'. <em>British Educational Research Journal</em>, 40(6), 917–936.</li>
            <li><strong>Selwyn, N. (2016).</strong> <em>Is Technology Good for Education?</em> Cambridge: Polity Press.</li>
            <li><strong>Sewell, T. (2021).</strong> <em>Commission on Race and Ethnic Disparities: The Report</em>. London: UK Cabinet Office.</li>
            <li><strong>Spivak, G. C. (1988).</strong> 'Can the Subaltern Speak?' In C. Nelson &amp; L. Grossberg (Eds.), <em>Marxism and the Interpretation of Culture</em> (pp. 271–313). Urbana: University of Illinois Press.</li>
            <li><strong>Ullman, J. (2021).</strong> <em>Free to Be? Exploring the Schooling Experiences of Australia's Sexuality and Gender Diverse High School Students</em>. Penrith: Western Sydney University.</li>
            <li><strong>Waslander, S., Pater, C., &amp; van der Weide, M. (2010).</strong> <em>Markets in Education: An Analytical Review of Empirical Research on Market Mechanisms in Education</em>. OECD Education Working Papers, No. 52. Paris: OECD Publishing.</li>
            <li><strong>Weber, M. (1978).</strong> <em>Economy and Society: An Outline of Interpretive Sociology</em> (G. Roth &amp; C. Wittich, Eds.). Berkeley: University of California Press. (Original work published 1922).</li>
            <li><strong>Williamson, B. (2017).</strong> <em>Big Data in Education: The Digital Future of Learning, Policy and Practice</em>. London: Sage Publications.</li>
            <li><strong>Willis, P. (1977).</strong> <em>Learning to Labour: How Working Class Kids Get Working Class Jobs</em>. Farnborough: Saxon House.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
            <li><strong>Zuboff, S. (2019).</strong> <em>The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power</em>. New York: PublicAffairs.</li>
        </ul>
    </section>
    <a href="core-concepts.html" class="back-link">&larr; Return to Core Concepts Index</a>
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

    files_to_generate = {
        root_directory / "core-concepts.html": generate_core_concepts_index_html(),
        root_directory / "module-1.html": generate_module_1_html(),
        root_directory / "module-2.html": generate_module_2_html(),
        root_directory / "module-3.html": generate_module_3_html(),
        root_directory / "module-4.html": generate_module_4_html(),
        root_directory / "module-5.html": generate_module_5_html(),
        root_directory / "module-6.html": generate_module_6_html(),
        root_directory / "module-7.html": generate_module_7_html(),
        root_directory / "bibliography.html": generate_bibliography_html(),
    }

    for file_path, content in files_to_generate.items():
        file_path.write_text(content, encoding="utf-8")
        print(f"Generated/Updated: {file_path.name}")

    commit_message = (
        "Add contextual module introduction cards to all section sub-pages\n\n"
        "Update core-concepts.html landing portal and all seven module pages\n"
        "with dedicated introductory overview cards and navigation links.\n\n"
        "- Ensure 100% citation-free markup."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
