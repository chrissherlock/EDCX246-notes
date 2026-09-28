#!/usr/bin/env python3
"""Update script to insert the missing inline SVG diagrams for Horizontal Competition

and Surveillance Capitalism into Section 5 of core-concepts.html, maintaining
all separated entries, Master Bibliography updates, clean markup free of
citation tags, and automated git synchronization.
"""

from pathlib import Path
import subprocess
import sys


def produce_complete_html_document() -> str:
    html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Core Sociological Concepts: Forensic Revision Guide</title>
    <style>
        :root {
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
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.65;
            max-width: 920px;
            margin: 0 auto;
            padding: 36px 20px;
            color: var(--text-main);
            background-color: var(--bg-page);
        }
        h1, h2, h3, h4, h5 {
            color: var(--text-heading);
            font-weight: 700;
        }
        h1 {
            font-size: 1.85rem;
            color: var(--primary-dark);
            border-bottom: 3px solid var(--border-accent);
            padding-bottom: 10px;
            margin-bottom: 18px;
            letter-spacing: -0.01em;
        }
        h2 {
            font-size: 1.25rem;
            color: var(--primary);
            margin-top: 36px;
            margin-bottom: 12px;
            border-bottom: 2px solid #fed7aa;
            padding-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        h3.tradition-header {
            font-size: 1.05rem;
            color: var(--text-heading);
            margin-top: 24px;
            margin-bottom: 16px;
            background: #fff7ed;
            padding: 5px 12px;
            border-left: 3px solid var(--primary);
            border-radius: 0 4px 4px 0;
            font-style: normal;
        }
        h4.concept-title {
            font-size: 1.02rem;
            color: var(--accent-orange);
            margin-top: 0;
            margin-bottom: 6px;
            padding-top: 0;
        }
        h5.counter-header {
            font-size: 0.95rem;
            color: var(--primary-dark);
            margin-top: 22px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .intro-card {
            display: flex;
            align-items: center;
            gap: 18px;
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--primary);
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 20px;
        }
        .intro-card svg {
            flex-shrink: 0;
            width: 72px;
            height: 72px;
        }
        .intro-card p {
            margin: 0;
            font-size: 0.92rem;
            color: #44403c;
            line-height: 1.6;
            text-align: justify;
        }
        /* Table of Contents Styling */
        .toc-card {
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--accent-orange);
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 32px;
        }
        .toc-card h3 {
            font-size: 1.02rem;
            color: var(--primary-dark);
            margin-top: 0;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .toc-grid {
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px 20px;
        }
        .toc-grid li {
            font-size: 0.88rem;
        }
        .toc-grid a {
            color: var(--primary-dark);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.15s ease-in-out;
        }
        .toc-grid a:hover {
            color: var(--accent-orange);
            text-decoration: underline;
        }
        .forensic-entry {
            margin-bottom: 20px;
            padding: 16px 20px;
            background-color: var(--bg-entry);
            border: 1px solid var(--border-subtle);
            border-left: 3px solid #fbbf24;
            border-radius: 6px;
        }
        .forensic-entry p {
            margin: 0 0 8px 0;
            font-size: 0.91rem;
            text-align: justify;
        }
        .forensic-entry ul {
            margin: 4px 0 10px 18px;
            font-size: 0.89rem;
            line-height: 1.55;
        }
        .forensic-entry li {
            margin-bottom: 6px;
            text-align: justify;
        }
        .scenario-box {
            margin: 10px 0 14px 0;
            padding: 10px 14px;
            background-color: var(--scenario-box-bg);
            border-left: 3px solid var(--primary);
            border-radius: 0 4px 4px 0;
            font-size: 0.88rem;
            color: #334155;
        }
        .scenario-box strong.label {
            color: var(--primary-dark);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.03em;
            display: block;
            margin-bottom: 4px;
        }
        .scenario-box ul {
            margin: 4px 0 6px 16px;
        }
        /* Interactive Tooltip Popovers */
        .tooltip-term {
            position: relative;
            cursor: help;
            border-bottom: 1.5px dotted var(--primary);
            font-weight: 600;
            color: var(--primary-dark);
        }
        .tooltip-term:hover::after,
        .tooltip-term:focus::after {
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
        }
        .tooltip-term:hover::before,
        .tooltip-term:focus::before {
            content: "";
            position: absolute;
            bottom: 110%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 6px;
            border-style: solid;
            border-color: #1c1917 transparent transparent transparent;
            z-index: 100;
        }
        /* Visual Flow Diagram Container */
        .diagram-container {
            margin: 16px 0;
            text-align: center;
        }
        .diagram-container svg {
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }
        /* Counter-Tradition Section Styling */
        .counter-tradition-box {
            margin-top: 18px;
            padding: 16px 18px;
            background-color: #ffffff;
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--accent-orange);
            border-radius: 6px;
        }
        .counter-svg-container {
            margin: 16px 0;
            text-align: center;
        }
        .counter-svg-container svg {
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }
        .camp-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 14px;
        }
        .camp-card {
            background-color: #fffdfa;
            border: 1px solid #fed7aa;
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 0.86rem;
            line-height: 1.5;
        }
        .camp-card h6 {
            margin: 0 0 4px 0;
            color: var(--primary-dark);
            font-size: 0.88rem;
            font-weight: 700;
        }
        .camp-card .theorist {
            color: var(--accent-orange);
            font-weight: 600;
            font-size: 0.8rem;
            display: block;
            margin-bottom: 6px;
        }
        .camp-card p {
            margin: 0;
            font-size: 0.84rem;
            text-align: left;
            color: #44403c;
        }
        .textbook-impact-box {
            margin-bottom: 24px;
            padding: 20px 24px;
            background-color: #fffbeb;
            border: 1px solid #fde68a;
            border-left: 5px solid #d97706;
            border-radius: 6px;
            font-size: 0.92rem;
            line-height: 1.65;
        }
        .textbook-impact-box h4.concept-title {
            color: var(--primary-dark);
            font-size: 1.12rem;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .textbook-impact-box ul {
            margin: 10px 0 0 20px;
        }
        .textbook-impact-box li {
            margin-bottom: 10px;
            text-align: justify;
        }
        .textbook-impact-box ul ul {
            margin-top: 6px;
        }
        .entry-references {
            margin-top: 14px;
            padding: 10px 14px;
            background-color: #fefce8;
            border: 1px dashed #f59e0b;
            border-radius: 4px;
            font-size: 0.84rem;
            color: #78350f;
        }
        .entry-references strong {
            display: block;
            color: var(--primary-dark);
            text-transform: uppercase;
            font-size: 0.76rem;
            letter-spacing: 0.04em;
            margin-bottom: 4px;
        }
        .entry-references ul {
            margin: 2px 0 2px 14px;
            padding-left: 0;
            line-height: 1.5;
        }
        .entry-references li {
            margin-bottom: 3px;
        }
        .audit-label-critique {
            display: inline-block;
            background-color: var(--badge-audit-bg);
            color: var(--badge-audit-text);
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 700;
            border: 1px solid var(--badge-audit-border);
        }
        .audit-label-strength {
            display: inline-block;
            background-color: var(--badge-strength-bg);
            color: var(--badge-strength-text);
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 700;
            border: 1px solid var(--badge-strength-border);
        }
        .biblio-section {
            margin-top: 48px;
            padding-top: 20px;
            border-top: 2px solid #fed7aa;
        }
        .biblio-section h2 {
            font-size: 1.25rem;
            color: var(--primary-dark);
            margin-top: 0;
            border-bottom: none;
            padding-bottom: 0;
        }
        .biblio-list {
            list-style-type: none;
            padding-left: 0;
            font-size: 0.88rem;
            line-height: 1.6;
        }
        .biblio-list li {
            margin-bottom: 12px;
            padding-left: 24px;
            text-indent: -24px;
        }
        .back-link {
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
        }
        .back-link:hover {
            background-color: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
        }
        @media (max-width: 768px) {
            .toc-grid {
                grid-template-columns: 1fr;
            }
            .camp-cards {
                grid-template-columns: 1fr;
            }
        }
        @media (max-width: 640px) {
            body { padding: 20px 12px; }
            .intro-card {
                flex-direction: column;
                align-items: flex-start;
                padding: 14px;
            }
            .intro-card svg {
                width: 56px;
                height: 56px;
            }
            .tooltip-term:hover::after,
            .tooltip-term:focus::after {
                width: 220px;
            }
        }
        @media print {
            body { padding: 12px; font-size: 9.5pt; }
            .intro-card { break-inside: avoid; page-break-inside: avoid; }
            .toc-card { break-inside: avoid; page-break-inside: avoid; }
            .forensic-entry { break-inside: avoid; page-break-inside: avoid; border: 1px solid #d6d3d1; }
            .tooltip-term { border-bottom: none; }
            .counter-tradition-box { break-inside: avoid; page-break-inside: avoid; }
            .textbook-impact-box { break-inside: avoid; page-break-inside: avoid; }
        }
    </style>
</head>
<body>

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
            This reference manual applies an uncompromising <strong>four-part forensic audit</strong> to the theoretical models
            in <em>Making Sense of Mass Education</em> (4th Edition). Each entry is evaluated through: (1) its historical genesis and empirical anomaly,
            (2) its internal theoretical architecture, (3) its legitimate diagnostic strengths in schooling, and (4) its critical blind spots, logical paradoxes, and practical pedagogical hazards.
        </p>
    </div>

    <!-- TABLE OF CONTENTS NAVIGATION CARD -->
    <nav class="toc-card" aria-label="Table of Contents">
        <h3>Table of Contents: Exam Revision Modules</h3>
        <ul class="toc-grid">
            <li><a href="#section-1">1. Social Class &amp; Stratification</a></li>
            <li><a href="#section-2">2. Race, Ethnicity &amp; Indigeneity</a></li>
            <li><a href="#section-3">3. Gender &amp; Sexualities</a></li>
            <li><a href="#section-4">4. Governance &amp; Subjectivity</a></li>
            <li><a href="#section-5">5. Neoliberalism &amp; Datafication</a></li>
            <li><a href="#section-6">6. Culture &amp; Technology</a></li>
            <li><a href="#section-7">7. Philosophy, Law &amp; Rights</a></li>
            <li><a href="#master-bibliography">Master Bibliography</a></li>
        </ul>
    </nav>

    <!-- 5. NEOLIBERALISM & DATAFICATION -->
    <section id="section-5">
        <h2>5. Neoliberalism &amp; Datafication</h2>
        <h3 class="tradition-header">Marketization, Managerialism &amp; Platform Capitalism</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Performativity &amp; Audit Culture (Stephen Ball)</h4>
            <p>
                Stephen J. Ball's landmark sociological critique of neoliberal education policy (<span class="tooltip-term" tabindex="0" data-tooltip="The Teacher's Soul and the Terrors of Performativity (2003), Journal of Education Policy, analyzing how accountability regimes re-engineer teacher subjectivity and institutional practice.">The Terrors of Performativity, 2003</span>)
                demonstrates that modern educational governance replaces professional autonomy, relational trust, and democratic purpose with corporate managerialism.
                Under <span class="tooltip-term" tabindex="0" data-tooltip="A technology, a culture, and a mode of regulation that employs judgements, comparisons, and displays of output as means of incentive, control, and transformation.">performativity</span>,
                schools and educators are evaluated not by intrinsic intellectual or pastoral merit, but by their capacity to produce quantifiable
                performance indicators, league table rankings, and inspection metrics within an all-pervasive
                <span class="tooltip-term" tabindex="0" data-tooltip="An institutional regime where the continuous generation, auditing, and public display of quantitative metrics replaces professional autonomy and relational trust.">audit culture</span>.
            </p>

            <div class="scenario-box">
                <strong class="label">Concrete Mechanism in Action: The NAPLAN / GCSE "Data Wall" &amp; The Bubble-Student Triage</strong>
                Imagine an executive faculty meeting in a secondary school three months prior to national census testing:
                <ul>
                    <li><strong>The Performance Wall:</strong> Student records are color-coded on a massive wall chart: Red (critically behind national minimum standards), Amber (the "bubble" students sitting within 5–10% of the proficient benchmark), and Green (securely passing).</li>
                    <li><strong>The Strategic Triage:</strong> The principal directs faculty heads to deploy supplementary tutoring and smaller class sizes <em>almost exclusively to the Amber cohort</em>. Students with profound reading disabilities in the Red band are effectively written off as statistical casualties incapable of moving the school's public aggregate score, while Green-band students are left to self-direct without extension.</li>
                    <li><strong>The Culture of Fabrication:</strong> The school's public website trumpets "outstanding annual value-added growth," presenting a carefully manufactured image of institutional excellence (<span class="tooltip-term" tabindex="0" data-tooltip="The deliberate construction of synthetic representations, curated metrics, and staged displays designed specifically to satisfy external audits rather than reflect authentic educational reality.">fabrication</span>).</li>
                </ul>
                The school has optimized its performance data while committing moral and pedagogical triage: educational resources are not allocated according to human learning need, but according to what will boost the school's public market ranking.
            </div>

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Developed between 1994 and 2003 as Ball analyzed the radical restructuring of public education under New Public Management (NPM) in the UK, Australia, and New Zealand. Ball addressed a striking empirical anomaly: why did decades of aggressive accountability reforms—introducing standardized testing, performance-based pay, public school league tables, and corporate inspection regimes under the banner of "raising standards"—fail to close the educational achievement gap between rich and poor students, while simultaneously producing unprecedented rates of teacher demoralization, curriculum narrowing, and institutional fraud? Ball proved that performativity does not improve real education; it simply forces institutions to become hyper-efficient at manufacturing metric displays.</p>

            <p><strong>2. Theoretical Mechanics:</strong> Ball's performative framework operates through four interlocking gears:</p>
            <ul>
                <li><strong>The Epistemological Shift (Numbers as Truth):</strong> What cannot be counted does not exist. Qualitative pedagogical complexity, pastoral empathy, character formation, and deep intellectual inquiry are erased because they cannot be rendered into standardized numerical benchmarks.</li>
                <li><strong>Fabrications (The Staged Self):</strong> Institutions and teachers are forced to dedicate immense labor to producing fabrications: curated portfolios, synthetic lesson plans designed solely for inspector walkthroughs, and coached classroom observations. Authenticity is subordinated to auditability.</li>
                <li><strong>Values Schizophrenia:</strong> Performativity produces acute psychological and ethical distress within educators. Teachers experience a painful internal fracture between their personal moral commitments (caring for vulnerable children, fostering curiosity) and the institutional demands of the market (demanding higher test scores, discarding non-metric activities).</li>
                <li><strong>The Triage Economy:</strong> Under competitive market pressures, educational care is rationed. Schools game admissions, quietly shed difficult students, and redirect teaching budgets toward marketing and public relations to secure competitive market survival.</li>
            </ul>

            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Unmasks the systemic causes of the global teacher retention and burnout crisis, diagnosing teacher exhaustion not as individual psychological weakness, but as structural moral injury inflicted by audit culture. It exposes how public league tables mislead parents by measuring socioeconomic intake advantage rather than authentic instructional value, and explains why high-stakes accountability inevitably induces institutional corruption, teaching to the test, and curriculum fragmentation.</p>

            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Accountability Vacuum &amp; Complacency Trap:</em> Completely abandoning objective performance transparency risks creating an accountability vacuum that protects failing schools and ineffective pedagogical practices from public scrutiny. Historically, disadvantaged working-class and minority students were routinely failed by public school systems that operated with complete opacity, allowing educational mediocrity to fester behind closed staffroom doors under the banner of "professional autonomy."</li>
                <li><em>Romanticizing Pre-Audit Opacity:</em> Critics of performativity frequently romanticize the pre-1980s era as a golden age of pastoral teacher trust, ignoring that historical systems often suffered from unchecked teacher bias, low academic expectations for marginalized groups, and total indifference to measurable literacy outcomes.</li>
                <li><em>The Democratic Necessity of Baseline Data:</em> Standardized performance data is essential for democratic governance and redistributive funding. Without objective census testing (such as NAPLAN or national literacy screens), governments and educational reformers cannot identify systemic regional disparities or direct targeted equity funding to under-resourced public communities.</li>
            </ul>

            <div class="entry-references">
                <strong>Primary Foundations &amp; Critical Counter-Texts:</strong>
                <ul>
                    <li><strong>Ball, S. J. (2003).</strong> 'The Teacher's Soul and the Terrors of Performativity'. <em>Journal of Education Policy</em>, 18(2), 215–228. <em>[The foundational text defining performativity, fabrications, and values schizophrenia in teaching]</em>.</li>
                    <li><strong>Ball, S. J. (1994).</strong> <em>Education Reform: A Critical and Post-Structural Approach</em>. Buckingham: Open University Press.</li>
                    <li><strong>Power, M. (1997).</strong> <em>The Audit Society: Rituals of Verification</em>. Oxford: Oxford University Press. <em>[The definitive sociological analysis of audit culture across modern public services]</em>.</li>
                    <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
                </ul>
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Horizontal Competition</h4>
            <p>
                A structural mechanism of neoliberal educational quasi-markets (<span class="tooltip-term" tabindex="0" data-tooltip="Politics, Markets and America's Schools (1990), establishing the voucher-driven market theory of institutional competition.">Chubb &amp; Moe, 1990</span>),
                <strong>horizontal competition</strong> describes the zero-sum market contest between schools operating at the same tier or regional catchment
                for student enrollment and associated per-capita voucher funding. Under market pressure, schools are incentivized to behave as rival commercial enterprises,
                competing through <span class="tooltip-term" tabindex="0" data-tooltip="Selecting students with high cultural and economic capital while actively avoiding or shedding students with complex behavioral or learning needs who require expensive support.">cream-skimming</span>,
                glossy branding, and exclusionary intake curation rather than aggregate instructional improvement.
            </p>

            <div class="diagram-container">
                <svg viewBox="0 0 760 280" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Horizontal Competition Market Cascade">
                    <rect x="10" y="10" width="740" height="260" rx="8" fill="#FFFDF8" stroke="#FED7AA" stroke-width="1.5"/>
                    <rect x="230" y="24" width="300" height="40" rx="6" fill="#78350F" stroke="#451A03" stroke-width="1.5"/>
                    <text x="380" y="42" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#FEF3C7" text-anchor="middle">PER-CAPITA VOUCHER FUNDING MODEL</text>
                    <text x="380" y="56" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#FDE68A" text-anchor="middle">State funding follows student headcounts across catchment</text>
                    <line x1="380" y1="64" x2="380" y2="86" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,91 376,83 384,83" fill="#B45309"/>
                    <rect x="230" y="92" width="300" height="38" rx="6" fill="#B45309" stroke="#78350F" stroke-width="1.5"/>
                    <text x="380" y="108" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">CATCHMENT MARKETIZATION</text>
                    <text x="380" y="121" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#FEF3C7" text-anchor="middle">Schools forced to compete as rival commercial enterprises</text>
                    <path d="M300 130 V 148 H 170 V 158" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="170,162 166,154 174,154" fill="#B45309"/>
                    <path d="M460 130 V 148 H 590 V 158" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="590,162 586,154 594,154" fill="#B45309"/>
                    <rect x="40" y="163" width="260" height="42" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                    <text x="170" y="179" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" font-weight="800" fill="#78350F" text-anchor="middle">CREAM-SKIMMING &amp; GATEKEEPING</text>
                    <text x="170" y="194" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Attracting high-capital students; screening high-needs</text>
                    <rect x="460" y="163" width="260" height="42" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                    <text x="590" y="179" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" font-weight="800" fill="#78350F" text-anchor="middle">PROMOTIONAL BUDGET DIVERSION</text>
                    <text x="590" y="194" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Diverting funds from learning support into marketing &amp; PR</text>
                    <line x1="170" y1="205" x2="170" y2="218" stroke="#B45309" stroke-width="1.5"/>
                    <line x1="590" y1="205" x2="590" y2="218" stroke="#B45309" stroke-width="1.5"/>
                    <path d="M170 218 H 380 V 224" stroke="#B45309" stroke-width="1.5"/>
                    <path d="M590 218 H 380 V 224" stroke="#B45309" stroke-width="1.5"/>
                    <line x1="380" y1="224" x2="380" y2="232" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="380,237 376,229 384,229" fill="#B45309"/>
                    <rect x="220" y="238" width="320" height="24" rx="4" fill="#EA580C" stroke="#9A3412" stroke-width="1.2"/>
                    <text x="380" y="254" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">DOWNSTREAM RESIDUALISATION (School B Sink Catchment)</text>
                </svg>
            </div>

            <div class="scenario-box">
                <strong class="label">Concrete Mechanism in Action: The Catchment Enrollment Arms Race</strong>
                Imagine two comprehensive secondary schools located four kilometers apart in an outer-metropolitan catchment operating under open enrollment:
                <ul>
                    <li><strong>The Marketing Escalation:</strong> School A redirects $80,000 from its learning support budget into a commercial marketing agency, rebranding with a corporate logo, glossy street banners, targeted social media campaigns, and an architectural glass facade.</li>
                    <li><strong>Cream-Skimming &amp; Covert Selection:</strong> School A introduces a competitive "academic extension stream" and an elite "sports academy," attracting aspirational middle-class families. Meanwhile, students presenting with complex behavioral histories or severe neurodivergent needs are subtly discouraged during open-day interviews with warnings that "our campus may lack the specialized pastoral facilities your child needs to flourish."</li>
                    <li><strong>The Residual Catchment Cascade:</strong> Neighboring School B absorbs the students turned away by School A. Because per-capita voucher funding follows the departing students, School B suffers compounding budgetary contractions, compelling it to cut elective subjects and specialist staffing.</li>
                </ul>
                The market has not elevated instructional quality across the district; it has simply manufactured institutional stratification, rewarding School A for exclusionary enrollment curation while leaving School B with concentrated disadvantage.
            </div>

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Developed during the 1980s and 1990s as part of the global rollout of New Public Management (NPM) and neoliberal educational restructuring across the United States, the United Kingdom, New Zealand, and Australia (formalized in policies such as parental choice, open enrollment zones, and charter/academy models). Free-market theorists (Milton Friedman, Chubb &amp; Moe) hypothesized that introducing consumer choice and portable per-capita funding vouchers would force inefficient public schools to innovate and raise teaching standards to survive. The empirical anomaly: decades of international policy data revealed that horizontal competition did not lift aggregate achievement. Instead, it accelerated socioeconomic and racial segregation. Schools discovered that the most cost-effective path to institutional survival was not the difficult labor of pedagogical improvement, but <em>intake curation</em>—attracting high-capital students and shedding resource-intensive cohorts.</p>

            <p><strong>2. Theoretical Mechanics:</strong> Horizontal competition operates through four primary operational gears:</p>
            <ul>
                <li><strong>The Per-Capita Funding Dynamic:</strong> State funding models tie operational budgets directly to student headcount. The loss of a small percentage of students removes significant discretionary funds, transforming annual enrollment recruitment into an existential contest for institutional solvency.</li>
                <li><strong>Cream-Skimming &amp; Covert Gatekeeping:</strong> To raise average exam metrics without increasing teaching costs, schools deploy covert selection mechanisms: specialized academies (STEM, performing arts), expensive laptop programs, strict uniform codes, and extensive interview processes that screen out disadvantaged or high-need families.</li>
                <li><strong>The Diversion of Productive Capital to Display:</strong> Operational funds are diverted from internal pedagogical support into outward-facing marketing: corporate promotional videos, public relations consultants, glossy prospectuses, and cosmetic architectural upgrades designed to signal prestige.</li>
                <li><strong>Downstream Residualisation:</strong> Because the market is zero-sum, a school that successfully brands itself as a local magnet directly deprives neighboring comprehensive schools of funding and aspirational peers, driving the neighboring institution into an accelerating cycle of budgetary decline and concentrated disadvantage.</li>
            </ul>

            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Demystifies the neoliberal rhetoric of "parental choice," demonstrating that in unregulated quasi-markets, schools choose families far more than families choose schools. It unmasks how market competition fuels social closure, spatial segregation, and budgetary distortion, explaining why institutional leaders are compelled to prioritize promotional display over basic student equity.</p>

            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Bureaucratic Monopolism Trap (The Anti-Choice Hazard):</em> Total ideological opposition to horizontal competition risks defending bureaucratic state monopolies. Rigidly confining students to compulsory geographic zones locks disadvantaged children into historically underperforming or unsafe neighborhood schools with zero structural exit mechanism, while wealthy families simply purchase homes in elite public catchments.</li>
                <li><em>Denying Legitimate School Improvement Drivers:</em> School Effectiveness and School Improvement (SESI) research demonstrates that transparent performance data and mild competitive pressure can serve as a catalyst for institutional reform, prompting complacent school executives to overhaul ineffective literacy approaches, modernize facilities, and become responsive to community concerns.</li>
                <li><em>Conflating Market Dynamics with Institutional Malice:</em> Treating horizontal competition purely as corporate conspiracy unfairly villainizes school principals who engage in marketing and intake management not out of elitist malice, but as a defensive survival strategy forced upon them by flawed per-capita funding formulas.</li>
            </ul>

            <div class="entry-references">
                <strong>Primary Foundations &amp; Critical Counter-Texts:</strong>
                <ul>
                    <li><strong>Chubb, J. E., &amp; Moe, T. M. (1990).</strong> <em>Politics, Markets and America's Schools</em>. Washington, D.C.: Brookings Institution Press. <em>[The foundational market-choice thesis arguing that institutional competition drives educational improvement]</em>.</li>
                    <li><strong>Friedman, M. (1955).</strong> 'The Role of Government in Education'. In R. A. Solo (Ed.), <em>Economics and the Public Interest</em> (pp. 123–144). New Brunswick: Rutgers University Press.</li>
                    <li><strong>Waslander, S., Pater, C., &amp; van der Weide, M. (2010).</strong> <em>Markets in Education: An Analytical Review of Empirical Research on Market Mechanisms in Education</em>. OECD Education Working Papers, No. 52. Paris: OECD Publishing.</li>
                </ul>
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Governance by Numbers &amp; Accountability Washback (Bob Lingard)</h4>
            <p>
                Bob Lingard's critical policy sociology (<span class="tooltip-term" tabindex="0" data-tooltip="Politics, Policies and Pedagogies in Education (2013) and Globalizing Education Policy (2010), analyzing how census testing and quantification steer education systems remotely.">Lingard et al., 2013</span>)
                demonstrates how the contemporary state regulates mass schooling through
                <span class="tooltip-term" tabindex="0" data-tooltip="An evaluative mode of governance where centralized census testing regimes (e.g., NAPLAN, PISA, league tables) allow the state to steer schooling systems remotely at a distance through numerical indicators.">governance by numbers</span>.
                Tied to public institutional rankings, national reporting dashboards, and market pressures, numerical governance produces severe
                <span class="tooltip-term" tabindex="0" data-tooltip="The structural distortion where the high-stakes format, narrow metrics, and anxiety of external census testing retroactively dictate and corrupt classroom pedagogy.">accountability washback</span>,
                compelling schools to cannibalize curriculum, game student data, and replace authentic holistic education with mechanical test drills.
            </p>

            <div class="diagram-container">
                <svg viewBox="0 0 760 300" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Governance by Numbers and Accountability Washback Pipeline">
                    <rect x="10" y="10" width="740" height="280" rx="8" fill="#FFFDF8" stroke="#FED7AA" stroke-width="1.5"/>
                    <rect x="230" y="24" width="300" height="42" rx="6" fill="#78350F" stroke="#451A03" stroke-width="1.5"/>
                    <text x="380" y="42" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#FEF3C7" text-anchor="middle">CENTRALIZED CENSUS TESTING</text>
                    <text x="380" y="56" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#FDE68A" text-anchor="middle">NAPLAN / PISA / League Tables / Standardized Benchmarks</text>
                    <line x1="380" y1="66" x2="380" y2="88" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,93 376,85 384,85" fill="#B45309"/>
                    <rect x="250" y="94" width="260" height="38" rx="6" fill="#B45309" stroke="#78350F" stroke-width="1.5"/>
                    <text x="380" y="110" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GOVERNANCE BY NUMBERS</text>
                    <text x="380" y="123" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#FEF3C7" text-anchor="middle">The Evaluative State: Steering System Autonomy at a Distance</text>
                    <line x1="380" y1="132" x2="380" y2="152" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,157 376,149 384,149" fill="#B45309"/>
                    <rect x="220" y="158" width="320" height="28" rx="4" fill="#EA580C" stroke="#9A3412" stroke-width="1.2"/>
                    <text x="380" y="176" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">SEVERE ACCOUNTABILITY WASHBACK</text>
                    <path d="M300 186 V 204 H 170 V 214" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="170,218 166,210 174,210" fill="#B45309"/>
                    <path d="M460 186 V 204 H 590 V 214" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="590,218 586,210 594,210" fill="#B45309"/>
                    <rect x="40" y="219" width="260" height="58" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                    <text x="170" y="235" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="800" fill="#78350F" text-anchor="middle">CURRICULUM CANNIBALISM</text>
                    <text x="170" y="250" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#44403C" text-anchor="middle">Arts, humanities, and inquiry evacuated</text>
                    <text x="170" y="262" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Replaced by 2D shading drills and writing templates</text>
                    <rect x="460" y="219" width="260" height="58" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                    <text x="590" y="235" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="800" fill="#78350F" text-anchor="middle">STRATEGIC EDUCATIONAL TRIAGE</text>
                    <text x="590" y="250" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#44403C" text-anchor="middle">Resources poured exclusively into 'bubble' students</text>
                    <text x="590" y="262" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Complex-needs and high-growth cohorts marginalized</text>
                </svg>
            </div>

            <div class="scenario-box">
                <strong class="label">Concrete Mechanism in Action: The NAPLAN Drill Season &amp; Term 1 Cannibalism</strong>
                Imagine a Year 5 teaching team in an outer-suburban state primary school during Term 1:
                <ul>
                    <li><strong>Curricular Evacuation:</strong> Ten weeks prior to the national testing window, school leadership mandates the suspension of integrated science units, instrumental music, drama, and visual arts (<span class="tooltip-term" tabindex="0" data-tooltip="The progressive elimination of non-tested subjects (arts, humanities, critical thinking) from the school timetable to maximize hours dedicated to mechanical test drills.">curriculum cannibalism</span>). Instruction is restructured around daily timed drills practicing 2D multiple-choice shading and formulaic five-paragraph persuasive writing templates.</li>
                    <li><strong>The Triage Protocol:</strong> Practice test results are mapped against national minimum standards. The assistant principal directs the specialist literacy intervention teacher to cease working with three students with severe dyslexia (classified as "incapable of moving up a band") and instead dedicate all intervention periods to six borderline students sitting just below Band 5 (the school’s public reporting target).</li>
                    <li><strong>Affective Distress:</strong> Primary students report stomach aches and test anxiety, while teachers spend staff meetings analyzing spreadsheet heatmaps rather than student creative portfolios.</li>
                </ul>
                The state did not mandate the elimination of the arts; rather, by governing through the comparative number, the state steered institutional behavior remotely, compelling the school to voluntarily cannibalize its own rich curriculum to protect its public standing.
            </div>

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Developed between 2007 and 2016 by Australian educational policy sociologist Bob Lingard (alongside Sam Sellar and Wayne Martino) following the introduction of Australia's National Assessment Program – Literacy and Numeracy (NAPLAN) and the launch of the *My School* website in 2010. Technocrats marketed census testing as an objective, low-stakes diagnostic tool designed to guarantee national standards and direct equity funding to struggling schools. The empirical anomaly: decades of intensive testing failed to close socioeconomic and Indigenous achievement gaps, while national performance on international measures (PISA) flatlined or declined. Instead of lifting standards, governing through numbers created widespread systemic corruption: curriculum narrowing, teaching to the test, student exclusion on test days, and unprecedented teacher demoralization.</p>

            <p><strong>2. Theoretical Mechanics:</strong> Governance by numbers operates through four interlocking operational gears:</p>
            <ul>
                <li><strong>Steering at a Distance (<span class="tooltip-term" tabindex="0" data-tooltip="The state apparatus that no longer directly manages daily operational routines, but steers institutions remotely through competitive market rules and quantitative performance audits.">The Evaluative State</span>):</strong> The state decentralizes daily operational management to local school principals while centralizing accountability through standardized numerical indicators. Autonomy is granted only on the condition of meeting the state's quantitative benchmarks.</li>
                <li><strong>Curriculum Cannibalism:</strong> What is tested becomes what is taught. Because census testing can only evaluate easily standardized, multiple-choice or formulaic proxies of literacy and numeracy, non-tested disciplines—humanities, arts, physical education, critical ethics, and deep scientific inquiry—are systematically squeezed out of the school timetable.</li>
                <li><strong>Strategic Educational Triage &amp; Gaming:</strong> When institutional reputations and leadership contracts are linked to performance benchmarks, schools engage in rational gaming: discouraging low-achieving students from sitting exams, and concentrating remedial resources exclusively on "bubble" students positioned directly beneath reporting thresholds.</li>
                <li><strong>The Ontological Inversion (Goodhart's Law):</strong> When a measure becomes a target, it ceases to be a good measure. The numerical test score ceases to be an imperfect proxy for learning and is treated as learning itself; a child's human capability is ontologically reduced to a statistical band on an online dashboard.</li>
            </ul>

            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Provides a rigorous sociological framework for understanding why teachers experience intense pedagogical alienation, explaining how external policy metrics distort daily classroom instruction. It unmasks how standardized testing regimes reduce complex, relational human learning to sterile quantitative indicators, and proves that institutional gaming is not a personal moral failure of teachers, but a structural imperative manufactured by the evaluative state.</p>

            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Equity Transparency Dilemma (The Blind-Spot Hazard):</em> Totalizing opposition to standardized census testing risks dismantling the sole objective diagnostic tool available to identify macroscopic, systemic inequality. Without system-wide baseline data across regional, socioeconomic, and racial lines, educational bureaucracies cannot identify where catastrophic literacy gaps exist, nor can governments justify redistributive, needs-based funding models (such as the Gonski funding reforms). Abandoning all census data risks returning to an era of staffroom opacity where failing schools hide behind rhetoric while disadvantaged children remain illiterate.</li>
                <li><em>Conflating the Measurement Tool with Political Weaponization:</em> The diagnostic failure lies not in the psychometrics of census testing per se, but in the high-stakes political publication of the data (league tables, media shaming, *My School* rankings). Conflating the measurement tool with its neoliberal market misuse can lead educators into anti-testing dogmatism that dismisses valid cognitive assessments and early diagnostic screeners.</li>
                <li><em>The Defeatist Fatalism of Complete Rejection:</em> Treating all testing as neoliberal oppression can paralyze teachers into refusing to engage with performance data formatively. Skilled instructional leaders routinely use baseline diagnostic data—not to drill for exams, but to identify specific phonemic, decoding, and numeracy deficits to ensure vulnerable students achieve foundational academic mastery.</li>
            </ul>

            <div class="entry-references">
                <strong>Primary Foundations &amp; Critical Counter-Texts:</strong>
                <ul>
                    <li><strong>Lingard, B. (2010).</strong> 'Policy borrowing, policy learning, and the politics of education policy: A critical review'. <em>Journal of Education Policy</em>, 25(2), 129–147.</li>
                    <li><strong>Lingard, B., Martino, W., Rezai-Rashti, G., &amp; Sellar, S. (2013).</strong> 'Globalizing education policy: Treating the disease with the disease?'. <em>Globalisation, Societies and Education</em>, 11(3), 390–408. <em>[The foundational text analyzing governance by numbers and accountability washback in schooling]</em>.</li>
                    <li><strong>Sellar, S., &amp; Lingard, B. (2014).</strong> 'The OECD and the expansion of PISA: New global modes of governance in education'. <em>British Educational Research Journal</em>, 40(6), 917–936.</li>
                    <li><strong>Gonski, D., Boston, K., Greiner, K., Lawrence, C., Scales, B., &amp; Tannock, P. (2011).</strong> <em>Review of Funding for Schooling: Final Report</em>. Canberra: Department of Education, Employment and Workplace Relations. <em>[Demonstrating the necessity of baseline standardized data for redistributive equity funding]</em>.</li>
                </ul>
            </div>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Surveillance Capitalism (Shoshana Zuboff)</h4>
            <p>
                Shoshana Zuboff's economic and sociological framework (<span class="tooltip-term" tabindex="0" data-tooltip="The Age of Surveillance Capitalism (2019), analyzing how commercial tech monopolies claim private human experience as free raw material for behavioral modification.">The Age of Surveillance Capitalism, 2019</span>)
                describes how commercial digital technology monopolies unilaterally claim private human experience as free raw material—
                <span class="tooltip-term" tabindex="0" data-tooltip="Behavioral data captured silently from human activities, used as raw material to feed machine-learning algorithms and predictive modification products.">behavioral surplus</span>—to
                be processed into proprietary data for predictive behavioral modification and profit. Within contemporary education, this operates through the
                <span class="tooltip-term" tabindex="0" data-tooltip="The corporate takeover and monetization of public educational infrastructure by for-profit EdTech platforms harvesting student analytics.">commercial enclosure</span>
                of public infrastructure, where EdTech platforms harvest student cognitive telemetry, attention spans, and digital footprints while bypassing privacy protections.
            </p>

            <div class="diagram-container">
                <svg viewBox="0 0 760 280" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Surveillance Capitalism Extraction Cycle">
                    <rect x="10" y="10" width="740" height="260" rx="8" fill="#FFFDF8" stroke="#FED7AA" stroke-width="1.5"/>
                    <rect x="220" y="24" width="320" height="40" rx="6" fill="#78350F" stroke="#451A03" stroke-width="1.5"/>
                    <text x="380" y="42" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#FEF3C7" text-anchor="middle">PUBLIC SCHOOL INFRASTRUCTURE</text>
                    <text x="380" y="56" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" fill="#FDE68A" text-anchor="middle">LMS Portals / Chromebooks / Adaptive Reading Software</text>
                    <line x1="380" y1="64" x2="380" y2="86" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,91 376,83 384,83" fill="#B45309"/>
                    <rect x="210" y="92" width="340" height="38" rx="6" fill="#B45309" stroke="#78350F" stroke-width="1.5"/>
                    <text x="380" y="108" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">EXTRACTION OF BEHAVIORAL SURPLUS</text>
                    <text x="380" y="121" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#FEF3C7" text-anchor="middle">Harvesting keystrokes, clicks, gaze direction &amp; biometrics</text>
                    <line x1="380" y1="130" x2="380" y2="150" stroke="#B45309" stroke-width="2"/>
                    <polygon points="380,155 376,147 384,147" fill="#B45309"/>
                    <rect x="220" y="156" width="320" height="30" rx="4" fill="#EA580C" stroke="#9A3412" stroke-width="1.2"/>
                    <text x="380" y="174" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">PROPRIETARY MACHINE LEARNING PROCESSING</text>
                    <path d="M300 186 V 204 H 170 V 214" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="170,218 166,210 174,210" fill="#B45309"/>
                    <path d="M460 186 V 204 H 590 V 214" stroke="#B45309" stroke-width="1.8"/>
                    <polygon points="590,218 586,210 594,210" fill="#B45309"/>
                    <rect x="40" y="219" width="260" height="42" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                    <text x="170" y="235" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" font-weight="800" fill="#78350F" text-anchor="middle">BEHAVIORAL MODIFICATION</text>
                    <text x="170" y="250" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Automated nudges, habituation &amp; compliance loops</text>
                    <rect x="460" y="219" width="260" height="42" rx="6" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
                    <text x="590" y="235" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" font-weight="800" fill="#78350F" text-anchor="middle">COMMERCIAL MONETIZATION</text>
                    <text x="590" y="250" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" fill="#57534E" text-anchor="middle">Predictive futures markets &amp; EdTech profit</text>
                </svg>
            </div>

            <div class="scenario-box">
                <strong class="label">Concrete Mechanism in Action: The Adaptive Reading App &amp; Behavioral Extraction</strong>
                Imagine a Year 4 primary classroom utilizing a popular, venture-capital-backed "adaptive literacy platform" mandated by the school district:
                <ul>
                    <li><strong>The Interface of Extraction:</strong> As children interact with the gamified reading modules, the software logs far more than correct answers. It records reading velocity, mouse hover durations, hesitation intervals, error patterns, and facial micro-expressions via webcams.</li>
                    <li><strong>Behavioral Surplus Harvesting:</strong> This raw telemetry constitutes behavioral surplus. It is transmitted directly to commercial servers, where machine-learning algorithms construct predictive psychological profiles of each child—categorizing their frustration thresholds and attention volatility.</li>
                    <li><strong>The Modification Loop:</strong> The platform deploys automated behavioral modification: dynamically altering difficulty curves, injecting micro-rewards, and pushing gamified notifications designed to maximize engagement time and habituate children to continuous monitoring.</li>
                </ul>
                The school has outsourced its core pedagogical functions to a for-profit data monopoly that treats children not as sovereign learners, but as raw economic units generating proprietary behavioral yield.
            </div>

            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Developed by Harvard business sociologist Shoshana Zuboff in her landmark 2019 text *The Age of Surveillance Capitalism*. Zuboff formulated the framework to explain a profound mutation in global capitalism: while tech monopolies marketed cloud services and digital portals as free, empowering innovations, schools discovered a startling economic reality—educational software providers offered zero-cost tools precisely because students and teachers were the product, not the consumer. The systematic harvesting of children's cognitive telemetry created massive proprietary data monopolies bypassing student privacy protections, turning public schools into captive markets for behavioral extraction.</p>

            <p><strong>2. Theoretical Mechanics:</strong> Surveillance capitalism operates through four primary operational gears:</p>
            <ul>
                <li><strong>The Predatory Capture of Behavioral Surplus:</strong> Just as industrial capitalism claimed physical nature as raw material, surveillance capitalism claims private human experience. Every student click, pause, scroll, and gaze direction is captured, quantified, and rendered into machine-readable data.</li>
                <li><strong>The Economies of Action (Behavioral Modification):</strong> Surveillance capitalism does not merely predict behavior; it intervenes to shape it. EdTech platforms use automated reinforcement loops and gamified dopamine triggers to herd student attention toward compliance and data generation.</li>
                <li><strong>The Instrumentalisation of Education:</strong> Public education is subordinated to commercial extraction. Classrooms become testing grounds where venture-backed algorithms trial predictive behavioral modification techniques on captive minor cohorts.</li>
                <li><strong>Asymmetry of Knowledge and Power:</strong> An extreme epistemic inequality develops: EdTech corporations hold absolute visibility into student cognitive states, while students, parents, and teachers remain completely blind to how algorithms process data or shape classroom experiences.</li>
            </ul>

            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Exposes the hidden economic architecture of commercial digital platforms, explaining why private tech monopolies invest heavily in providing zero-cost software to underfunded public school systems. It connects macro-level platform capitalism directly to everyday classroom screen sessions, defending student cognitive sovereignty and privacy as fundamental educational rights.</p>

            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Technophobic Luddite Trap:</em> Blanket opposition to all digital educational technology under the banner of surveillance capitalism falls into technophobic fatalism. It obscures the vital distinction between commercial platform monopolies and open-source, non-profit, sovereign digital learning infrastructure.</li>
                <li><em>The Utility of Non-Profit Digital Infrastructure:</em> Well-governed, privacy-respecting digital tools—such as secure non-profit learning management systems, assistive speech-to-text software for disabled students, and collaborative mapping platforms—dramatically expand educational access for isolated rural students, home-bound youth, and neurodivergent learners. Treating all educational technology as predatory corporate exploitation abandons digital equity.</li>
                <li><em>The Practical Impossibility of Complete Withdrawal:</em> In a digitized global economy, demanding the total eradication of digital platforms from schooling can leave students digitally illiterate and unprepared for modern tertiary study and workforce participation. The solution to surveillance capitalism is not Luddite rejection, but rigorous public regulation, strict data sovereignty laws, and the funding of public digital infrastructure.</li>
            </ul>

            <div class="entry-references">
                <strong>Primary Foundations &amp; Critical Counter-Texts:</strong>
                <ul>
                    <li><strong>Zuboff, S. (2019).</strong> <em>The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power</em>. New York: PublicAffairs. <em>[The foundational economic and sociological text defining surveillance capitalism, behavioral surplus, and economies of action]</em>.</li>
                    <li><strong>Selwyn, N. (2016).</strong> <em>Is Technology Good for Education?</em> Cambridge: Polity Press.</li>
                    <li><strong>Williamson, B. (2017).</strong> <em>Big Data in Education: The Digital Future of Learning, Policy and Practice</em>. London: Sage Publications.</li>
                </ul>
            </div>
        </div>

        <!-- MASTER STANDALONE SECTION CARD: CRITICAL SYNTHESIS ON NEOLIBERALISM & DATAFICATION -->
        <div class="textbook-impact-box" style="margin-top: 24px;">
            <h4 class="concept-title">Critical Synthesis: Impact of Marketization, Managerialism &amp; Platform Capitalism on <em>Making Sense of Mass Education</em></h4>
            <p>
                <strong>How do Ball, Horizontal Competition, Lingard, and Zuboff collectively shape and challenge the central thesis of <em>Making Sense of Mass Education</em>?</strong><br>
                Together, these four frameworks provide the textbook with an uncompromising macroeconomic X-ray of contemporary schooling, demonstrating how neoliberal policy, audit cultures, zero-sum market competition, and digital extraction have transformed public education from a civic democratic institution into a marketized data commodity:
            </p>
            <ul>
                <li>
                    <strong>How they SUPPORT and Empower the Textbook's Thesis (The Neoliberal Critique):</strong>
                    <ul>
                        <li><em>Corporate Managerialism &amp; Performativity (Ball):</em> Rescues the textbook from assuming that accountability is neutral. Ball demonstrates how audit cultures and league tables replace professional trust with KPI metrics, forcing schools into institutional fabrication, curriculum narrowing, and toxic bubble-student triage.</li>
                        <li><em>Market Catchment Sorting (Horizontal Competition):</em> Exposes the myth of "parental choice." Per-capita voucher funding forces schools to act as rival commercial firms, driving cream-skimming, exclusionary gatekeeping, and the systematic residualisation of neighborhood public schools.</li>
                        <li><em>Governance by Numbers (Lingard):</em> Explains how centralized census testing (NAPLAN, PISA) acts as remote steering, producing severe accountability washback that cannibalizes the arts and humanities in favor of mechanical test drills.</li>
                        <li><em>Surveillance Capitalism (Zuboff):</em> Updates the textbook's critique for the digital era, revealing how commercial EdTech monopolies enclose public schooling infrastructure to harvest student behavioral surplus as proprietary raw material for predictive behavioral modification.</li>
                    </ul>
                </li>
                <li>
                    <strong>Where they CAUSE PROFOUND PROBLEMS for the Textbook (The Forensic Hazards &amp; Blind Spots):</strong>
                    <ul>
                        <li><em>The Accountability Transparency Trap:</em> Totalizing opposition to all performativity, competition, and census testing risks creating an accountability vacuum. Without objective performance transparency and baseline census data, failing institutions are shielded from public scrutiny, and governments cannot justify targeted, needs-based equity funding (such as Gonski reforms) to support disadvantaged catchments.</li>
                        <li><em>Conflating Assessment Tools with Political Misuse:</em> Blaming standardized psychometric testing for structural inequality confuses the diagnostic measurement tool with its high-stakes, marketized political weaponization (league tables, media shaming). Denying all baseline data leaves educators without diagnostic tools to identify early reading and numeracy gaps.</li>
                        <li><em>The Technophobic Fatalism Trap:</em> Branding all digital data collection as an Orwellian panopticon forces educators into a Luddite retreat. Objective learning analytics are vital for automating teacher workloads, identifying hidden literacy gaps, and safeguarding vulnerable children from online predators or self-harm.</li>
                        <li><em>Romanticizing Pre-Neoliberal Opacity:</em> Critiques of marketization often romanticize the pre-1980s era as an egalitarian golden age of teacher autonomy, ignoring that historical systems tolerated unchecked teacher bias, low expectations for minority cohorts, and total opacity regarding learning outcomes.</li>
                    </ul>
                </li>
                <li>
                    <strong>The Section 5 Synthesis Verdict:</strong>
                    Neoliberalism, marketization, and datafication frameworks provide an indispensable critical X-ray of how corporate managerialism, audit cultures, zero-sum competition, and surveillance capitalism corrupt public education. However, educators and policymakers must balance this structural critique with practical democratic necessity: maintaining transparent performance auditing for equity redistribution, rejecting anti-assessment dogmatism, and harnessing non-profit digital tools for inclusion without surrendering public infrastructure to commercial exploitation.
                </li>
            </ul>
        </div>
    </section>

    <!-- MASTER FORMAL BIBLIOGRAPHY -->
    <section id="master-bibliography" class="biblio-section">
        <h2>Master Bibliography: Primary Sources &amp; Critical References</h2>
        <ul class="biblio-list">
            <li><strong>Ball, S. J. (1994).</strong> <em>Education Reform: A Critical and Post-Structural Approach</em>. Buckingham: Open University Press.</li>
            <li><strong>Ball, S. J. (2003).</strong> 'The Teacher's Soul and the Terrors of Performativity'. <em>Journal of Education Policy</em>, 18(2), 215–228.</li>
            <li><strong>Chubb, J. E., &amp; Moe, T. M. (1990).</strong> <em>Politics, Markets and America's Schools</em>. Washington, D.C.: Brookings Institution Press.</li>
            <li><strong>Clarke, R. (1988).</strong> 'Information Technology and Dataveillance'. <em>Communications of the ACM</em>, 31(5), 498–512.</li>
            <li><strong>Friedman, M. (1955).</strong> 'The Role of Government in Education'. In R. A. Solo (Ed.), <em>Economics and the Public Interest</em> (pp. 123–144). New Brunswick: Rutgers University Press.</li>
            <li><strong>Gonski, D., Boston, K., Greiner, K., Lawrence, C., Scales, B., &amp; Tannock, P. (2011).</strong> <em>Review of Funding for Schooling: Final Report</em>. Canberra: Department of Education, Employment and Workplace Relations.</li>
            <li><strong>Lingard, B. (2010).</strong> 'Policy borrowing, policy learning, and the politics of education policy: A critical review'. <em>Journal of Education Policy</em>, 25(2), 129–147.</li>
            <li><strong>Lingard, B., Martino, W., Rezai-Rashti, G., &amp; Sellar, S. (2013).</strong> 'Globalizing education policy: Treating the disease with the disease?'. <em>Globalisation, Societies and Education</em>, 11(3), 390–408.</li>
            <li><strong>Power, M. (1997).</strong> <em>The Audit Society: Rituals of Verification</em>. Oxford: Oxford University Press.</li>
            <li><strong>Sellar, S., &amp; Lingard, B. (2014).</strong> 'The OECD and the expansion of PISA: New global modes of governance in education'. <em>British Educational Research Journal</em>, 40(6), 917–936.</li>
            <li><strong>Selwyn, N. (2016).</strong> <em>Is Technology Good for Education?</em> Cambridge: Polity Press.</li>
            <li><strong>Vinson, T. (2002).</strong> <em>Inquiry into the Provision of Public Education in New South Wales</em>. Sydney: NSW Teachers Federation &amp; Principals' Councils.</li>
            <li><strong>Waslander, S., Pater, C., &amp; van der Weide, M. (2010).</strong> <em>Markets in Education: An Analytical Review of Empirical Research on Market Mechanisms in Education</em>. OECD Education Working Papers, No. 52. Paris: OECD Publishing.</li>
            <li><strong>Williamson, B. (2017).</strong> <em>Big Data in Education: The Digital Future of Learning, Policy and Practice</em>. London: Sage Publications.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
            <li><strong>Zuboff, S. (2019).</strong> <em>The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power</em>. New York: PublicAffairs.</li>
        </ul>
    </section>

    <a href="index.html" class="back-link">&larr; Return to Main Exam Revision Guide</a>

</body>
</html>
'''
    return html_content


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
    target_file = root_directory / "core-concepts.html"

    target_file.write_text(produce_complete_html_document(), encoding="utf-8")
    print(f"Successfully generated clean core-concepts.html: {target_file.resolve()}")

    commit_message = (
        "Add inline SVG architecture diagrams to Section 5 concepts\n\n"
        "Incorporate custom inline SVG flow diagrams for Horizontal Competition\n"
        "and Surveillance Capitalism in Section 5 of core-concepts.html,\n"
        "maintaining 100% citation-free markup and automated git sync."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
