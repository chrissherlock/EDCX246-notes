#!/usr/bin/env python3
"""Regenerate the EDCX246 exam revision guide as a modular 7-page site with

an index portal, dedicated module pages, and automated git synchronization.
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
            align-items: center;
            gap: 18px;
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--primary);
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 20px;
        }}
        .intro-card svg {{
            flex-shrink: 0;
            width: 72px;
            height: 72px;
        }}
        .intro-card p {{
            margin: 0;
            font-size: 0.92rem;
            color: #44403c;
            line-height: 1.6;
            text-align: justify;
        }}
        /* Table of Contents Styling */
        .toc-card {{
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--accent-orange);
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 32px;
        }}
        .toc-card h3 {{
            font-size: 1.02rem;
            color: var(--primary-dark);
            margin-top: 0;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .toc-grid {{
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px 20px;
        }}
        .toc-grid li {{
            font-size: 0.88rem;
        }}
        .toc-grid a {{
            color: var(--primary-dark);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.15s ease-in-out;
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
        /* Interactive Tooltip Popovers */
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
        /* Visual Flow Diagram Container */
        .diagram-container {{
            margin: 16px 0;
            text-align: center;
        }}
        .diagram-container svg {{
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }}
        /* Counter-Tradition Section Styling */
        .counter-tradition-box {{
            margin-top: 18px;
            padding: 16px 18px;
            background-color: #ffffff;
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--accent-orange);
            border-radius: 6px;
        }}
        .counter-svg-container {{
            margin: 16px 0;
            text-align: center;
        }}
        .counter-svg-container svg {{
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
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
        .back-link {{
            display: inline-block;
            margin-top: 28px;
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
            .toc-grid {{
                grid-template-columns: 1fr;
            }}
            .camp-cards {{
                grid-template-columns: 1fr;
            }}
        }}
        @media (max-width: 640px) {{
            body {{ padding: 20px 12px; }}
            .intro-card {{
                flex-direction: column;
                align-items: flex-start;
                padding: 14px;
            }}
            .intro-card svg {{
                width: 56px;
                height: 56px;
            }}
            .tooltip-term:hover::after,
            .tooltip-term:focus::after {{
                width: 220px;
            }}
        }}
        @media print {{
            body {{ padding: 12px; font-size: 9.5pt; }}
            .intro-card {{ break-inside: avoid; page-break-inside: avoid; }}
            .toc-card {{ break-inside: avoid; page-break-inside: avoid; }}
            .forensic-entry {{ break-inside: avoid; page-break-inside: avoid; border: 1px solid #d6d3d1; }}
            .tooltip-term {{ border-bottom: none; }}
            .counter-tradition-box {{ break-inside: avoid; page-break-inside: avoid; }}
            .textbook-impact-box {{ break-inside: avoid; page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
"""


def generate_index_html() -> str:
    html = get_common_head("Core Sociological Concepts: Exam Revision Portal")
    html += r"""
    <h1>EDCX246 Exam Revision Guide: Forensic Concept Analysis</h1>

    <div class="intro-card">
        <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Forensic Dossier Icon">
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
        <p>
            Welcome to the modular exam revision portal for <em>Making Sense of Mass Education</em> (4th Edition).
            Select a module below to access comprehensive forensic dossiers, interactive tooltips, visual architecture diagrams,
            and critical textbook syntheses.
        </p>
    </div>

    <!-- TABLE OF CONTENTS NAVIGATION CARD -->
    <nav class="toc-card" aria-label="Table of Contents">
        <h3>Index: Exam Revision Modules</h3>
        <ul class="toc-grid">
            <li><a href="module-1.html">1. Social Class &amp; Stratification</a></li>
            <li><a href="module-2.html">2. Race, Ethnicity &amp; Indigeneity</a></li>
            <li><a href="module-3.html">3. Gender &amp; Sexualities</a></li>
            <li><a href="module-4.html">4. Governance &amp; Subjectivity</a></li>
            <li><a href="module-5.html">5. Neoliberalism &amp; Datafication</a></li>
            <li><a href="module-6.html">6. Culture &amp; Technology</a></li>
            <li><a href="module-7.html">7. Philosophy, Law &amp; Rights</a></li>
            <li><a href="bibliography.html">Master Bibliography</a></li>
        </ul>
    </nav>
</body>
</html>
"""
    return html


def generate_module_1_html() -> str:
    html = get_common_head("Module 1: Social Class & Stratification")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-1">
        <h2>1. Social Class &amp; Educational Stratification</h2>
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

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Developed during the 1960s by Pierre Bourdieu and Jean-Claude Passeron in post-WWII France. State technocrats had eliminated university tuition fees, anticipating that open financial access would establish a pure meritocracy. However, statistical surveys revealed a glaring contradiction: despite free tuition, working-class and peasant students failed and withdrew at dramatically higher rates than bourgeois cohorts. Classical Marxism attributed reproduction almost exclusively to economic capital (property, wealth, and ownership of the means of production), but Bourdieu recognized that financial explanations could not account for why working-class students with adequate funding still struggled with the implicit cultural demands of the academy. Expanding capital into the cultural sphere, the term was formally introduced in print in the 1973 essay <em>Cultural Reproduction and Social Reproduction</em> and later codified into three states in the 1986 essay <em>The Forms of Capital</em>.</p>

            <p><strong>2. Theoretical Mechanics &amp; Advanced Operational Gears:</strong> Bourdieu's foundational texts establish four precise operational gears governing cultural capital:</p>
            <ul>
                <li><strong>The Economy of Time &amp; "Wasted Time":</strong> Accumulating embodied capital (<em>Bildung</em>) requires personal labor-time that cannot be delegated. Because children of educated families begin accumulating usable cultural currency from birth, they gain an insurmountable head start. For the working-class child, early domestic socialization represents what Bourdieu terms <em>"wasted time"</em> in the eyes of the school—time that must be expensively spent unlearning, correcting, and retraining home speech patterns and postures. Furthermore, accumulating cultural capital requires <em>free time</em>—the suspension of economic urgency that only affluent families can purchase.</li>
                <li><strong>The Three Interdependent States (The Ancient Greek Analogy):</strong>
                    <ul>
                        <li><span class="tooltip-term" tabindex="0" data-tooltip="The internal software: vocabulary, accent, posture, and conversational confidence wired into your brain and body over years. Like knowing how to read ancient Greek.">Embodied State (État Incorporé)</span>: <strong>The personal skills, habits, and fluency carried inside you.</strong> This is the mental and bodily software: your vocabulary, accent, conversational ease, posture, and unthinking confidence when speaking to authority. It cannot be handed over like cash; it takes years of personal labor-time to absorb at home. Like knowing how to read ancient Greek, it is physically wired into your nervous system and dies with you.</li>
                        <li><span class="tooltip-term" tabindex="0" data-tooltip="Physical objects requiring skill to decode: books, grand pianos, art, lab gear. Cash buys the object, but only embodied skill lets you play or read it.">Objectified State (État Objectivé)</span>: <strong>Physical cultural possessions.</strong> Books, art collections, grand pianos, classical music recordings, and scientific instruments. Anyone with lottery winnings can buy a grand piano with cash (economic capital), but it remains an expensive piece of furniture unless someone in the house has the <em>embodied</em> skill to sit down and play Beethoven on it.</li>
                        <li><span class="tooltip-term" tabindex="0" data-tooltip="Official paper certificates: degrees, diplomas, licenses. Proves competence on paper so you don't have to re-prove your worth every single morning.">Institutionalized State (État Institutionalisé)</span>: <strong>Official qualifications and credentials.</strong> University degrees, diplomas, and state licenses. An uncertified genius must prove their skill from scratch to every employer they meet. But an official degree from an elite university acts as a state-guaranteed stamp of approval, setting an employee's salary and market value on paper without requiring daily proof.</li>
                    </ul>
                </li>
                <li><strong>The Intraclass Divide (Teachers vs. Industrialists):</strong> The ruling class is not monolithic; it is split between the <em>dominant fraction</em> (rich in economic capital, poorer in cultural capital, e.g., corporate heads and commercial executives) and the <em>dominated fraction</em> (rich in cultural capital, poorer in economic capital, e.g., academics, teachers, and artistic producers). Because schooling is run by the cultural fraction, the academic market rewards its own domestic culture above all else. This explains why teachers' children consistently outperform the children of wealthy commercial executives on purely academic tests.</li>
                <li><strong>Credential Devaluation &amp; Defensive Escalation:</strong> Educational qualifications derive their market exchange value from their <strong>scarcity</strong>. When democratic access expands the supply of basic university degrees, qualifications undergo inevitable inflation and currency devaluation. The dominant classes preserve social closure not by opposing mass education, but by dynamically <em>escalating the threshold</em> of entry:
                    <ul>
                        <li><em>Vertical Reconversion &amp; Pedigree:</em> Shifting the baseline goalposts from basic bachelor's degrees to costly postgraduate degrees, elite MBAs, and hyper-selective institutional tiers (e.g., French <em>Grandes Écoles</em>, Oxbridge, or Ivy League networks) that remain disproportionately monopolized by high-capital families.</li>
                        <li><em>The Retreat to Informal Gatekeeping:</em> As paper qualifications equalize across applicants, employers pivot hiring criteria away from tested technical competence toward non-scholastic filters: unpaid corporate internships (which only wealthy families can financially subsidize), inherited social connections, and the evaluation of <span class="tooltip-term" tabindex="0" data-tooltip="Bodily mannerisms, unthinking confidence, accent, and conversational ease evaluated as 'culture fit'.">embodied 'interview poise'</span> and 'culture fit'—rubrics that covertly reward bourgeois domestic habitus over scholastic effort.</li>
                    </ul>
                </li>
            </ul>

            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Dismantles the naive meritocracy myth by demonstrating how schools convert inherited class familiarity into academic merit. It exposes why purely material interventions (hardware rollouts, fee waivers) consistently fail to close equity gaps if implicit curriculum and assessment expectations remain unexamined. It accurately diagnoses how subjective, open-ended grading rubrics penalize working-class students for lacking conversational ease and bourgeois manual/linguistic mannerisms.</p>

            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Relativist Trap (Conflating Arbitrary Culture with Powerful Knowledge):</em> Bourdieu treats curriculum content as an arbitrary ruling-class power tool. However, formal logic, standard grammatical syntax, the calculus, and empirical science are not arbitrary cultural toys; they are objective cognitive amplifiers that allow humans to model, manipulate, and master the material and social world. Treating all curricula as arbitrary class violence collapses the vital distinction between arbitrary manners and empirically grounded, powerful knowledge (Michael Young).</li>
                <li><em>The Delpit Dilemma &amp; Monday Morning Catastrophe:</em> As African-American educational scholar Lisa Delpit demonstrated, when progressive educators stop explicitly teaching standard grammar and academic rhetoric under the guise of avoiding cultural violence, they do not liberate marginalized kids; they strand them. Middle-class kids acquire the dominant codes at home, while disadvantaged kids are denied the explicit instruction needed to enter higher education and professional fields.</li>
                <li><em>The Intraclass Paradox:</em> If schooling is driven by the cultural fraction (teachers) against the economic fraction (industrialists), the curriculum cannot be characterized simply as a monolithic ruling-class conspiracy. It is an arena of conflict where teachers routinely promote critical inquiry, social mobility, and democratic debate against purely commercial demands.</li>
                <li><em>Structural Fatalism &amp; Pedagogical Defeatism:</em> Bourdieu's model operates as an unbroken reproduction loop that minimizes student agency and high-expectations teaching. Empirically, cognitive psychology and explicit instruction research demonstrate that structured, systematic teaching dramatically accelerates domain learning, disproving Bourdieu's assumption that working-class children cannot overcome the domestic time-gap.</li>
            </ul>

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

                <div class="camp-cards">
                    <div class="camp-card">
                        <h6>1. The Epistemic Strike</h6>
                        <span class="theorist">Michael Young (2008)</span>
                        <p>
                            Bourdieu treats academic knowledge as arbitrary ruling-class etiquette. Young demonstrates
                            the vital boundary between <em>Knowledge of the Powerful</em> (bourgeois accents, social manners)
                            and <em>Powerful Knowledge</em> (calculus, thermodynamics, historical evidence). Disciplinary
                            knowledge is testable and universally reliable; denying it to the poor in the name of
                            "anti-elitism" disarms them intellectually.
                        </p>
                    </div>
                    <div class="camp-card">
                        <h6>2. The Pedagogical Strike</h6>
                        <span class="theorist">Lisa Delpit (1988, 1995)</span>
                        <p>
                            Progressive educators inspired by reproduction theory abandoned explicit grammar and direct
                            instruction to avoid "imposing symbolic violence." Delpit proves that middle-class kids
                            learn the "culture of power" at home, leaving poor and minority students stranded.
                            True educational equity requires unapologetic, structured instruction in the dominant code.
                        </p>
                    </div>
                    <div class="camp-card">
                        <h6>3. The Philosophical Strike</h6>
                        <span class="theorist">Jacques Rancière (1983 / 2004)</span>
                        <p>
                            Bourdieu asserts that the working class is "complicit" in its oppression via unconscious
                            misrecognition. Rancière unmasks this as profound sociological paternalism: it frames
                            workers as blind dupes unable to perceive reality until an enlightened sociologist demystifies
                            it for them. In practice, students recognize structural hypocrisy with immense clarity.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Habitus (Pierre Bourdieu)</h4>
            <p>
                Habitus is the <strong>social muscle memory</strong> of human action. Just as an experienced tennis player
                does not pause mid-rally to calculate physics formulas or consult an instruction manual, a person moves through
                the social world guided by an internalized, subconscious <span class="tooltip-term" tabindex="0" data-tooltip="An intuitive 'feel for the game' operating automatically without conscious mental calculation.">"feel for the game" (sens pratique)</span>.
                It is the permanent software installed in your nervous system by the class conditions of your upbringing.
            </p>

            <div class="scenario-box">
                <strong class="label">Concrete Mechanism in Action: Habitus in the Corridor</strong>
                Imagine how two students respond when a teacher announces a harsh, unexpected assignment deadline:
                <ul>
                    <li><strong>Middle-Class Habitus (Julian):</strong> Grew up in a home where rules were negotiated and adult authority was reasoned with. His gut reaction is relaxed entitlement: he instinctively approaches the teacher after class, maintains confident eye contact, and politely negotiates an extension. He navigates the school <em>"like a fish in water."</em></li>
                    <li><strong>Working-Class Habitus (Marcus):</strong> Grew up in an environment where adult directives were non-negotiable and challenging authority invited trouble. His gut reaction is protective silence: he accepts the failing mark or quietly disengages, thinking, <em>"That's just how the system is; what's the point of arguing?"</em></li>
                </ul>
                Neither student calculated their response using a conscious strategy. Their background simply generated an immediate, physical, and unthinking sense of what is possible, reasonable, and safe to do.
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Symbolic Violence &amp; Misrecognition (Pierre Bourdieu &amp; Jean-Claude Passeron)</h4>
            <p>
                Symbolic violence is <strong>power without physical force</strong>. Instead of using police, threats, or guns,
                ruling groups maintain dominance quietly through everyday rules, expectations, and cultural standards.
                Crucially, this system relies on <span class="tooltip-term" tabindex="0" data-tooltip="Failing to recognize that social rules are rigged; mistaking arbitrary upper-class standards for natural talent and objective fairness.">misrecognition (méconnaissance)</span>
                and <span class="tooltip-term" tabindex="0" data-tooltip="Unknowingly going along with your own oppression because you believe the system is fair and neutral.">complicity</span>:
                because ordinary people are tricked into believing that the rules are natural and fair, they blame themselves
                when they fail rather than questioning the system.
            </p>
        </div>

        <!-- RE-SCOPED BOURDIEUSIAN CRITICAL SYNTHESIS CARD -->
        <div class="textbook-impact-box">
            <h4 class="concept-title">Critical Synthesis: Impact on <em>Making Sense of Mass Education</em> (The Bourdieusian Paradigm)</h4>
            <p>
                <strong>Is the textbook's reliance on Bourdieu right, wrong, or fatally incomplete?</strong><br>
                Evaluating the Bourdieusian pillar within <em>Making Sense of Mass Education</em> requires testing its reproduction thesis against its primary educational merits and its dangerous pedagogical hazards:
            </p>
            <ul>
                <li>
                    <strong>Where Bourdieu EMPOWERS the Textbook's Thesis (The Diagnostic Core):</strong>
                    <ul>
                        <li><em>Demolishing Naive Meritocracy:</em> Cultural Capital provides the textbook with its sharpest weapon to disprove the claim that schools are neutral playing fields. It explains why purely material access (free tuition, digital devices) consistently fails to close equity gaps if implicit curriculum and assessment expectations remain unexamined.</li>
                        <li><em>Explaining Dislocation without Deficit (Habitus):</em> Accounts for student alienation and voluntary self-elimination—the belief that higher education is <em>"not for the likes of us"</em>—without pathologizing students' raw cognitive capability.</li>
                        <li><em>Unmasking Symbolic Violence:</em> Explains how unequal educational sorting preserves democratic legitimacy because students misrecognize class-biased curricula as reflections of innate talent and individual moral failure.</li>
                    </ul>
                </li>
                <li>
                    <strong>Where Bourdieu ENDANGERS the Textbook's Thesis (The Critical Hazards):</strong>
                    <ul>
                        <li><em>The Epistemic Relativist Trap (Michael Young):</em> Treating curriculum content as an arbitrary ruling-class power tool collapses the distinction between arbitrary manners and <strong>Powerful Knowledge</strong>. Disciplinary knowledge (calculus, thermodynamics, historical evidence) provides objective intellectual leverage; denying it to disadvantaged children in the name of anti-elitism disarms them intellectually.</li>
                        <li><em>The Delpit Dilemma:</em> Lisa Delpit demonstrated that when progressive educators refuse to explicitly teach standard grammar and academic rhetoric to avoid "symbolic violence," they abandon disadvantaged children. Affluent children acquire these codes at home; disadvantaged children master them only through direct, unapologetic instruction.</li>
                        <li><em>Structural Fatalism &amp; Paternalism:</em> Bourdieu's model operates as an unbroken reproduction loop that ignores cognitive science and explicit instruction research proving that systematic teaching accelerates learning. Furthermore, Jacques Rancière unmasks Bourdieu's concept of "misrecognition" as condescending paternalism that reduces working-class agents to unconscious cultural dupes.</li>
                    </ul>
                </li>
                <li>
                    <strong>The Forensic Verdict on the Bourdieusian Paradigm:</strong>
                    Bourdieu's reproduction model within the textbook is <strong>indispensable as an anatomical X-ray of inherited privilege, but toxic as a standalone pedagogical compass</strong>. It correctly diagnoses how schools unconsciously reward domestic bourgeois socialization, but it fails whenever it is used to justify lowered academic expectations, curriculum relativism, or defeatist fatalism.
                </li>
            </ul>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_module_2_html() -> str:
    html = get_common_head("Module 2: Race, Ethnicity & Indigeneity")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-2">
        <h2>2. Race, Ethnicity &amp; Indigeneity</h2>
        <h3 class="tradition-header">Postcolonial &amp; Critical Race Paradigms</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Colonisation of the Mind (Frantz Fanon)</h4>
            <p>
                Frantz Fanon's psychoanalytic and anti-colonial framework (<span class="tooltip-term" tabindex="0" data-tooltip="Black Skin, White Masks (Peau noire, masques blancs, 1952), exploring the psychiatric distortions inflicted on colonized subjects by white imperial culture.">Black Skin, White Masks, 1952</span>)
                demonstrates that colonial subjugation operates not merely through territorial occupation or military coercion, but through the psychic colonization of
                the colonized subject's interiority. Imperial schooling operates as a central apparatus of psychological subjugation, compelling racialized learners
                to internalize an <span class="tooltip-term" tabindex="0" data-tooltip="The internalization of racial subordination as an inescapable bodily defect, leading racialized subjects to perceive their own skin and heritage as inferior.">epidermalization of inferiority</span>
                while striving for <span class="tooltip-term" tabindex="0" data-tooltip="The neurotic psychological and behavioral drive of colonized subjects to 'whiten' their speech, tastes, and mannerisms to gain validation from the colonizer.">lactification</span>
                (psychic whitening) through assimilation into European linguistic and epistemological codes.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Epistemic Violence (Gayatri Spivak)</h4>
            <p>
                Gayatri Chakravorty Spivak's postcolonial feminist thesis (<span class="tooltip-term" tabindex="0" data-tooltip="Can the Subaltern Speak? (1988), analyzing the discursive silencing of colonized subjects within imperial historiography and law.">Can the Subaltern Speak?, 1988</span>)
                demonstrates that imperialism does not conquer solely through military invasion or administrative rule, but through
                <span class="tooltip-term" tabindex="0" data-tooltip="The systematic destruction, invalidation, and delegitimation of a colonized society's knowledge frameworks, philosophy, and ways of understanding reality.">epistemic violence</span>:
                the institutional silencing, delegitimation, and destruction of non-Western knowledge traditions by dominant colonial epistemologies that masquerade
                as universal rationality.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Institutional Racism &amp; Whiteness as Policy (David Gillborn)</h4>
            <p>
                David Gillborn's Critical Race Theory (CRT) framework (<span class="tooltip-term" tabindex="0" data-tooltip="Racism and Education: Coincidence or Conspiracy? (2008), establishing CRT in UK and Commonwealth educational policy sociology.">Racism and Education, 2008</span>)
                demonstrates that educational racism is not an aberrant departure from an otherwise fair system, nor is it reducible to isolated interpersonal bigotry by individual "bad apple" teachers.
                Instead, racism is an ordinary, deep-seated, and permanent operational baseline of modern schooling.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Culturally Sustaining Pedagogy (Django Paris &amp; H. Samy Alim)</h4>
            <p>
                Pioneered by Django Paris (<span class="tooltip-term" tabindex="0" data-tooltip="Culturally Sustaining Pedagogy (2012), published in Educational Researcher.">Paris, 2012</span>)
                and elaborated alongside H. Samy Alim (<span class="tooltip-term" tabindex="0" data-tooltip="Culturally Sustaining Pedagogies (2017).">Paris &amp; Alim, 2014, 2017</span>),
                <span class="tooltip-term" tabindex="0" data-tooltip="An educational framework requiring schools to actively perpetuate and foster linguistic, literate, and cultural pluralism as sovereign intellectual heritage.">Culturally Sustaining Pedagogy (CSP)</span>
                requires schools not merely to acknowledge minority cultural practices, but to actively perpetuate, sustain, and revitalize them as sovereign intellectual heritage.
            </p>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_module_3_html() -> str:
    html = get_common_head("Module 3: Gender & Sexualities")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-3">
        <h2>3. Gender &amp; Sexualities</h2>
        <h3 class="tradition-header">Structural Gender Orders &amp; Poststructuralist Performativity</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Gender Regimes &amp; Hegemonic Masculinity (Raewyn Connell)</h4>
            <p>
                Raewyn Connell's sociology of the gender order posits that gender is not a fixed biological dichotomy or simple sex role, but an evolving historical structure of power, labor, emotional investment, and symbolism. At the apex of this institutionalized hierarchy sits
                <span class="tooltip-term" tabindex="0" data-tooltip="The culturally idealized form of manhood in a given time and place that legitimizes global male dominance over women.">hegemonic masculinity</span>.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Gender Performativity (Judith Butler)</h4>
            <p>
                Judith Butler's poststructuralist feminist thesis (<span class="tooltip-term" tabindex="0" data-tooltip="Gender Trouble (1990), decoupling gender and sex from biological essentialism.">Gender Trouble, 1990</span>)
                demonstrates that gender is fundamentally
                <span class="tooltip-term" tabindex="0" data-tooltip="An act that brings into being what it names; repeating normative gestures and codes produces the retroactive illusion of an internal essence.">performative</span>:
                an ongoing, stylized repetition of bodily gestures, speech acts, and regulatory citations that retroactively produces the illusion of an innate, internal gender identity.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Compulsory Heterosexuality (Adrienne Rich)</h4>
            <p>
                Adrienne Rich's radical feminist critique (<span class="tooltip-term" tabindex="0" data-tooltip="Compulsory Heterosexuality and Lesbian Existence (1980).">Rich, 1980</span>)
                demonstrates that heterosexuality is not an innate biological preference or natural human default, but an institutionalized, coercive
                <span class="tooltip-term" tabindex="0" data-tooltip="An institutional apparatus engineered by law, economy, and culture to enforce social conformity, female domestic subservience, and male dominance.">political apparatus</span>.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Minority Stress &amp; Affirmative Pedagogy (Ilan Meyer)</h4>
            <p>
                The synthesis of Ilan Meyer's public health psychiatric framework (<span class="tooltip-term" tabindex="0" data-tooltip="Prejudice, Social Stress, and Mental Health in Lesbian, Gay, and Bisexual Populations (2003).">Minority Stress Model, 2003</span>)
                with critical educational theory establishes that the elevated rates of psychological distress experienced by LGBTQ+ students are the chronic psychological toll of enduring hostile institutional environments.
            </p>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_module_4_html() -> str:
    html = get_common_head("Module 4: Governance & Subjectivity")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-4">
        <h2>4. Governance, Surveillance &amp; Subjectivity</h2>
        <h3 class="tradition-header">The Foucaultian Architecture of Power</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Disciplinary Power &amp; Docile Bodies (Michel Foucault)</h4>
            <p>
                Michel Foucault's genealogy of modern disciplinary power (<span class="tooltip-term" tabindex="0" data-tooltip="Discipline and Punish (1975), tracing the micro-physics of disciplinary training.">Discipline and Punish, 1975</span>)
                demonstrates that power in modern institutions operates across a
                <span class="tooltip-term" tabindex="0" data-tooltip="A fine-grained, pervasive capillary network of disciplinary techniques applied directly to human bodies.">micro-physics of power</span>
                that meticulously trains, optimizes, and coordinates the human body, manufacturing <span class="tooltip-term" tabindex="0" data-tooltip="Bodies rendered economically useful and politically obedient through training.">docile bodies</span>.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">The Panopticon &amp; The Disciplinary Triad (Michel Foucault)</h4>
            <p>
                Describes how modern institutions replace physical coercion with
                <span class="tooltip-term" tabindex="0" data-tooltip="The architectural principle where the permanent possibility of unverifiable observation compels individuals to internalize surveillance and self-police.">panopticism</span>,
                operating alongside hierarchical observation, normalizing judgment, and the examination to transform human subjects into self-regulating entities.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Governmentality &amp; Technologies of the Self (Michel Foucault)</h4>
            <p>
                Foucault's formulation of <span class="tooltip-term" tabindex="0" data-tooltip="The 'conduct of conduct': governing populations at a distance by shaping the field of possible action.">governmentality</span>
                and <span class="tooltip-term" tabindex="0" data-tooltip="Techniques that permit individuals to effect operations on their bodies and souls to achieve self-transformation.">technologies of the self</span>,
                where neoliberal subjects voluntarily audit and optimize themselves as "entrepreneurs of the self."
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">The Psy-Complex &amp; Medicalisation of Deviance (Nikolas Rose / Peter Conrad)</h4>
            <p>
                Reveals how modern schooling redefines behavioral non-compliance and pedagogical mismatch as organic psychiatric pathologies (e.g., ADHD) through the
                <span class="tooltip-term" tabindex="0" data-tooltip="The heterogeneous network of psychologists, standardized rating scales, and diagnostic manuals that govern subjectivity.">psy-complex</span>.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Digital Panopticon &amp; Dataveillance</h4>
            <p>
                The ubiquitous algorithmic monitoring of student cognitive, behavioral, and physical presence across school and domestic environments through
                <span class="tooltip-term" tabindex="0" data-tooltip="The systematic monitoring of people through digital trails, metadata, keystrokes, and LMS telemetry.">dataveillance</span>.
            </p>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_module_5_html() -> str:
    html = get_common_head("Module 5: Neoliberalism & Datafication")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-5">
        <h2>5. Neoliberalism &amp; Datafication</h2>
        <h3 class="tradition-header">Marketization, Managerialism &amp; Platform Capitalism</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Performativity &amp; Audit Culture (Stephen Ball)</h4>
            <p>
                Stephen J. Ball's sociological critique (<span class="tooltip-term" tabindex="0" data-tooltip="The Terrors of Performativity (2003).">Ball, 2003</span>)
                demonstrates that modern educational governance replaces professional autonomy with
                <span class="tooltip-term" tabindex="0" data-tooltip="A mode of regulation that employs judgements, comparisons, and displays of output as means of incentive, control, and transformation.">performativity</span>
                and an all-pervasive <span class="tooltip-term" tabindex="0" data-tooltip="An institutional regime where the continuous generation of quantitative metrics replaces professional trust.">audit culture</span>.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Horizontal Competition</h4>
            <p>
                A structural mechanism of neoliberal educational quasi-markets (<span class="tooltip-term" tabindex="0" data-tooltip="Politics, Markets and America's Schools (1990).">Chubb &amp; Moe, 1990</span>)
                describing zero-sum market contests between schools competing through
                <span class="tooltip-term" tabindex="0" data-tooltip="Selecting students with high cultural and economic capital while actively avoiding or shedding high-need students.">cream-skimming</span> and branding.
            </p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Governance by Numbers &amp; Accountability Washback (Bob Lingard)</h4>
            <p>
                Bob Lingard's framework (<span class="tooltip-term" tabindex="0" data-tooltip="Globalizing Education Policy (2013).">Lingard et al., 2013</span>)
                describing how centralized census testing steers education systems remotely through <span class="tooltip-term" tabindex="0" data-tooltip="An evaluative mode of governance using quantitative indicators.">governance by numbers</span>, producing severe <span class="tooltip-term" tabindex="0" data-tooltip="The structural distortion where testing metrics retroactively corrupt classroom pedagogy.">accountability washback</span>.
            </p>
            <div class="diagram-container">
                <svg viewBox="0 0 760 300" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Governance by Numbers Pipeline">
                    <rect x="10" y="10" width="740" height="280" rx="8" fill="#FFFDF8" stroke="#FED7AA" stroke-width="1.5"/>
                    <rect x="230" y="24" width="300" height="42" rx="6" fill="#78350F" stroke="#451A03" stroke-width="1.5"/>
                    <text x="380" y="42" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#FEF3C7" text-anchor="middle">CENTRALIZED CENSUS TESTING</text>
                    <text x="380" y="56" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#FDE68A" text-anchor="middle">NAPLAN / PISA / League Tables / Standardized Benchmarks</text>
                    <line x1="380" y1="66" x2="380" y2="88" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,93 376,85 384,85" fill="#B45309"/>
                    <rect x="250" y="94" width="260" height="38" rx="6" fill="#B45309" stroke="#78350F" stroke-width="1.5"/>
                    <text x="380" y="110" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GOVERNANCE BY NUMBERS</text>
                    <text x="380" y="123" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#FEF3C7" text-anchor="middle">The Evaluative State: Steering System Autonomy at a Distance</text>
                </svg>
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Surveillance Capitalism (Shoshana Zuboff)</h4>
            <p>
                Shoshana Zuboff's framework (<span class="tooltip-term" tabindex="0" data-tooltip="The Age of Surveillance Capitalism (2019).">Zuboff, 2019</span>)
                describes how commercial tech monopolies claim private human experience as <span class="tooltip-term" tabindex="0" data-tooltip="Behavioral data captured silently from human activities, used as raw material for predictive modification products.">behavioral surplus</span>
                for predictive modification and profit through <span class="tooltip-term" tabindex="0" data-tooltip="The corporate takeover and monetization of public educational infrastructure.">commercial enclosure</span>.
            </p>
        </div>

        <!-- MASTER STANDALONE SECTION CARD: CRITICAL SYNTHESIS ON NEOLIBERALISM & DATAFICATION -->
        <div class="textbook-impact-box" style="margin-top: 24px;">
            <h4 class="concept-title">Critical Synthesis: Impact of Marketization, Managerialism &amp; Platform Capitalism on <em>Making Sense of Mass Education</em></h4>
            <p>
                Neoliberal policy, audit cultures, zero-sum market competition, and digital extraction have transformed public education from a civic democratic institution into a marketized data commodity.
            </p>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_module_6_html() -> str:
    html = get_common_head("Module 6: Culture & Technology")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-6">
        <h2>6. Culture &amp; Technology</h2>
        <h3 class="tradition-header">Media Studies, Subcultural Agency &amp; Cognitive Ecology</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Active Audience Theory &amp; Polysemy (Stuart Hall)</h4>
            <p>
                Stuart Hall's cultural studies framework (<span class="tooltip-term" tabindex="0" data-tooltip="Encoding/Decoding (1980).">Hall, 1980</span>)
                demonstrates that media texts are <span class="tooltip-term" tabindex="0" data-tooltip="Bearing multiple, competing potential meanings rather than a single fixed message.">polysemic</span>
                and actively negotiated by audiences through dominant-hegemonic, negotiated, or oppositional stances.
            </p>
            <div class="diagram-container">
                <svg viewBox="0 0 760 300" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Stuart Hall Encoding Decoding Circuit Diagram">
                    <rect x="10" y="10" width="740" height="280" rx="8" fill="#FFFDF8" stroke="#FED7AA" stroke-width="1.5"/>
                    <rect x="230" y="24" width="300" height="42" rx="6" fill="#78350F" stroke="#451A03" stroke-width="1.5"/>
                    <text x="380" y="42" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#FEF3C7" text-anchor="middle">MOMENT OF ENCODING (PRODUCTION)</text>
                    <text x="380" y="56" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#FDE68A" text-anchor="middle">Institutional frameworks, relations of production &amp; preferred meanings</text>
                    <line x1="380" y1="66" x2="380" y2="88" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,93 376,85 384,85" fill="#B45309"/>
                    <rect x="250" y="94" width="260" height="38" rx="6" fill="#B45309" stroke="#78350F" stroke-width="1.5"/>
                    <text x="380" y="110" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">POLYSEMIC MEDIA TEXT</text>
                    <text x="380" y="123" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#FEF3C7" text-anchor="middle">A structured sign vehicle carrying multiple potential decodings</text>
                </svg>
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Semiotic Democracy &amp; Textual Poaching (John Fiske)</h4>
            <p>John Fiske's concept that youth audiences actively seize corporate cultural products (memes, fashion, video games), remixing and subverting corporate signs to construct autonomous meaning.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Intertextuality &amp; Moral Panics (Julia Kristeva / Stanley Cohen)</h4>
            <p>Kristeva's textual mosaic concept alongside Cohen's sociological model of media-manufactured societal panics framing youth behaviors or educational standards as existential threats.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Media Ecology &amp; The Social Model of Disability (Neil Postman / Mike Oliver)</h4>
            <p>Postman's Faustian analysis of technological trade-offs paired with Oliver's social model defining disability as an institutional mismatch with inaccessible environments.</p>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_module_7_html() -> str:
    html = get_common_head("Module 7: Philosophy, Law & Rights")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
    <section id="section-7">
        <h2>7. Philosophy, Law &amp; Educational Rights</h2>
        <h3 class="tradition-header">Critical Praxis, Ethics &amp; Jurisprudence</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Critical Pedagogy &amp; Praxis (Paulo Freire)</h4>
            <p>Paulo Freire's critique (<em>Pedagogy of the Oppressed</em>, 1968) of the 'banking model' of education in favor of problem-posing dialogue, conscientisation (critical consciousness), and praxis (uniting reflection and action for liberation).</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Normative Ethics &amp; Relational Care (Nel Noddings / Aristotle)</h4>
            <p>The philosophical synthesis of Kantian deontology (treating learners as ends, never as means), Aristotelian phronesis (practical wisdom), and Nel Noddings' ethics of care grounded in attentiveness and trust.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Non-Delegable Duty of Care &amp; Negligence</h4>
            <p>The common law tort doctrine imposing an affirmative, non-delegable duty upon schools and teachers to take reasonable precautions against foreseeable risks of physical and psychiatric harm.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">UNCRC Article 12 &amp; Participatory Rights</h4>
            <p>The United Nations Convention on the Rights of the Child (1989), specifically Article 12 guaranteeing children the right to express their views freely in all matters affecting them.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Regimes of Truth vs. Powerful Knowledge (Michel Foucault / Michael Young)</h4>
            <p>The intellectual tension between Foucault's poststructuralist assertion that all knowledge is a power-laden 'regime of truth,' and Michael Young's Social Realism defending universal access to 'powerful knowledge'—specialized, discipline-grounded knowledge.</p>
        </div>
    </section>
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


def generate_bibliography_html() -> str:
    html = get_common_head("Master Bibliography: Primary Sources & References")
    html += r"""
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
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
    <a href="index.html" class="back-link">&larr; Return to Index Portal</a>
</body>
</html>
"""
    return html


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
        root_directory / "index.html": generate_index_html(),
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
        print(f"Generated: {file_path.name}")

    commit_message = (
        "Modularize revision guide into 7 module pages and index portal\n\n"
        "Split core-concepts.html into an index portal (index.html), seven\n"
        "modular section pages (module-1.html to module-7.html), and a master\n"
        "bibliography page (bibliography.html), maintaining clean citation-free markup."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
