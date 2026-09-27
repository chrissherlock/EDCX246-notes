#!/usr/bin/env python3
"""Upgrade Cultural Capital in core-concepts.html to a bulletproof forensic dossier

incorporating primary source mechanics and a formal bibliography.
"""

from pathlib import Path
import subprocess
import sys


def produce_complete_html_document() -> str:
    template = r'''<!DOCTYPE html>
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
        h1, h2, h3, h4 {
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
        .intro-card {
            display: flex;
            align-items: center;
            gap: 18px;
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--primary);
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 24px;
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
        .forensic-entry {
            margin-bottom: 16px;
            padding: 14px 18px;
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
            margin-bottom: 4px;
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
        }
        @media print {
            body { padding: 12px; font-size: 9.5pt; }
            .intro-card { break-inside: avoid; page-break-inside: avoid; }
            .forensic-entry { break-inside: avoid; page-break-inside: avoid; border: 1px solid #d6d3d1; }
        }
    </style>
</head>
<body>

    <h1>EDCX246 Exam Revision Guide: Forensic Concept Analysis</h1>

    <div class="intro-card">
        <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Forensic Dossier Icon">
            <!-- Back Folder Flap (Rich Muted Manila Stock) -->
            <path d="M14 26C14 22.6863 16.6863 20 20 20H44L52 30H100C103.314 30 106 32.6863 106 36V90C106 93.3137 103.314 96 100 96H20C16.6863 96 14 93.3137 14 90V26Z" fill="#D97706"/>
            <!-- Paper Sheet 2 (Underlying Soft Cream Sheet) -->
            <rect x="25" y="22" width="70" height="68" rx="3" fill="#F5F5F4" stroke="#D6D3D1" stroke-width="1.2"/>
            <!-- Paper Sheet 1 (Main Document) -->
            <rect x="29" y="15" width="70" height="75" rx="3" fill="#FFFFFF" stroke="#A8A29E" stroke-width="1.2"/>
            <!-- Dossier Header & Text Lines -->
            <line x1="38" y1="27" x2="65" y2="27" stroke="#B45309" stroke-width="2.5" stroke-linecap="round"/>
            <line x1="38" y1="35" x2="88" y2="35" stroke="#78716C" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="38" y1="41" x2="84" y2="41" stroke="#A8A29E" stroke-width="1.3" stroke-linecap="round"/>
            <line x1="38" y1="47" x2="76" y2="47" stroke="#A8A29E" stroke-width="1.3" stroke-linecap="round"/>
            <!-- Subtle Red Stamp Badge -->
            <rect x="58" y="55" width="34" height="15" rx="2" fill="#FFF1F2" stroke="#BE123C" stroke-width="1.2"/>
            <text x="61" y="66" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8" font-weight="700" fill="#BE123C" letter-spacing="0.8">AUDIT</text>
            <!-- Front Folder Flap (Warm Deep Amber) -->
            <path d="M12 44C12 40.6863 14.6863 38 18 38H102C105.314 38 108 40.6863 108 44L103 94C103 97.3137 100.314 100 97 100H23C19.6863 100 17 97.3137 17 94L12 44Z" fill="#B45309"/>
            <!-- Folder Fastener Clasp -->
            <circle cx="60" cy="52" r="4.5" fill="#FEF3C7" stroke="#78350F" stroke-width="1.5"/>
            <line x1="60" y1="48" x2="60" y2="56" stroke="#78350F" stroke-width="1.5"/>
            <!-- Forensic Inspection Magnifying Lens -->
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

    <!-- 1. SOCIAL CLASS & STRATIFICATION -->
    <section>
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
                <li><strong>The Economy of Time &amp; "Wasted Time":</strong> Accumulating embodied capital (*Bildung*) requires personal labor-time that cannot be delegated. Because children of educated families begin accumulating usable cultural currency from birth, they gain an insurmountable head start. For the working-class child, early domestic socialization represents what Bourdieu terms <em>"wasted time"</em> in the eyes of the school—time that must be expensively spent unlearning, correcting, and retraining home speech patterns and postures. Furthermore, accumulating cultural capital requires <em>free time</em>—the suspension of economic urgency that only affluent families can purchase.</li>
                <li><strong>The Three Interdependent States:</strong>
                    <ul>
                        <li><em>Embodied State (État Incorporé):</em> Long-lasting dispositions of mind and body (syntax, accent, posture, bodily hexis). Fused to the biological individual; dies with the bearer.</li>
                        <li><em>Objectified State (État Objectivé):</em> Material cultural goods (classical texts, paintings, instruments, laboratory equipment). Transmissible legally via economic capital, but requiring embodied capital to decode and appropriate symbolically.</li>
                        <li><em>Institutionalized State (État Institutionalisé):</em> Legally sanctioned academic qualifications that convert embodied cultural capital into a state-guaranteed currency with fixed conversion rates on the occupational labor market.</li>
                    </ul>
                </li>
                <li><strong>The Intraclass Divide (Teachers vs. Industrialists):</strong> The ruling class is not monolithic; it is split between the <em>dominant fraction</em> (rich in economic capital, poorer in cultural capital, e.g., corporate heads and commercial executives) and the <em>dominated fraction</em> (rich in cultural capital, poorer in economic capital, e.g., academics, teachers, and artistic producers). Because schooling is run by the cultural fraction, the academic market rewards its own domestic culture above all else. This explains why teachers' children consistently outperform the children of wealthy commercial executives on purely academic tests.</li>
                <li><strong>Credential Devaluation &amp; Escalation:</strong> When democratic educational expansion increases the volume of basic university degrees, qualifications undergo inflation. The dominant classes preserve social closure by escalating credential thresholds—retreating into postgraduate degrees, elite institutional pedigrees (e.g., Grandes Écoles, Oxbridge), and non-scholastic criteria such as interview poise, accent, and social capital.</li>
            </ul>

            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Dismantles the naive meritocracy myth by demonstrating how schools convert inherited class familiarity into academic merit. It exposes why purely material interventions (hardware rollouts, fee waivers) consistently fail to close equity gaps if implicit curriculum and assessment expectations remain unexamined. It accurately diagnoses how subjective, open-ended grading rubrics penalize working-class students for lacking conversational ease and bourgeois mannerisms.</p>

            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Relativist Trap (Conflating Arbitrary Culture with Powerful Knowledge):</em> Bourdieu treats curriculum content as an arbitrary ruling-class power tool. However, formal logic, standard grammatical syntax, the calculus, and empirical science are not arbitrary cultural toys; they are objective cognitive amplifiers that allow humans to model, manipulate, and master the material and social world. Treating all curricula as arbitrary class violence collapses the vital distinction between arbitrary manners and empirically grounded, powerful knowledge (Michael Young).</li>
                <li><em>The Delpit Dilemma &amp; Monday Morning Catastrophe:</em> As African-American educational scholar Lisa Delpit demonstrated, when progressive educators stop explicitly teaching standard grammar and academic rhetoric under the guise of avoiding cultural violence, they do not liberate marginalized kids; they strand them. Middle-class kids acquire the dominant codes at home, while disadvantaged kids are denied the explicit instruction needed to enter higher education and professional fields.</li>
                <li><em>The Intraclass Paradox:</em> If schooling is driven by the cultural fraction (teachers) against the economic fraction (industrialists), the curriculum cannot be characterized simply as a monolithic ruling-class conspiracy. It is an arena of conflict where teachers routinely promote critical inquiry, social mobility, and democratic debate against purely commercial demands.</li>
                <li><em>Structural Fatalism &amp; Pedagogical Defeatism:</em> Bourdieu's model operates as an unbroken reproduction loop that minimizes student agency and high-expectations teaching. Empirically, cognitive psychology and explicit instruction research demonstrate that structured, systematic teaching dramatically accelerates domain learning, disproving Bourdieu's assumption that working-class children cannot overcome the domestic time-gap.</li>
            </ul>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Habitus (Pierre Bourdieu)</h4>
            <p>Habitus denotes a system of durable, transposable dispositions—internalized perceptual schemes, bodily stances, and subconscious inclinations—acquired through immersion in a specific class position. It functions as an unreflective practical sense (<em>sens pratique</em>) or 'feel for the game' that steers individual practices without conscious calculation.</p>
            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Forged in Bourdieu's ethnographic studies of the Kabyle peasantry during the Algerian war of independence (late 1950s) and rural bachelorhood in his native Béarn. Bourdieu sought to break the French intellectual deadlock between Claude Lévi-Strauss's structuralism (which treated humans as passive automatons executing cultural rules) and Jean-Paul Sartre's existentialism (which asserted radical, unconstrained personal freedom). Algerian peasants could not simply choose to become industrial wage earners, nor were they running automated scripts; their traditional rural temporalities and honor codes clashed with the colonial money economy. Codified in <em>Outline of a Theory of Practice</em> (1972/1977) and <em>The Logic of Practice</em> (1980).</p>
            <p><strong>2. Theoretical Mechanics:</strong> Defined as <em>'structured structures predisposed to function as structuring structures.'</em> It internalizes the objective probabilities and class boundaries of childhood into mental templates (structured structure), which then generate thoughts, tastes, and actions that mirror those limits (structuring structure). It is deeply somaticized as <em>bodily hexis</em> (posture, gait, vocal tension, space utilization).</p>
            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Explains institutional affinity versus dislocation. Middle-class children navigate school with intuitive ease because their home habitus mirrors institutional culture. Explains self-elimination without overt coercion: working-class students internalize objective limits into subjective preferences (the feeling that higher education is <em>'not for the likes of us'</em>), walking away from academic pathways voluntarily.</p>
            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Béarn Postman Paradox (Performative Self-Contradiction):</em> If habitus is an inescapable, totalizing conditioning cage, how did Pierre Bourdieu—the son of an uneducated, low-ranking provincial postal worker in rural Béarn—ascend to the absolute summit of the elite French academy? If one person can transcend their originating habitus through intellectual discipline and public schooling, habitus is not an unbroken deterministic cycle; schooling can function as an engine of emancipation, not merely reproduction.</li>
                <li><em>The Hysteresis Inadequacy:</em> Bourdieu's concept of hysteresis (the lag when habitus fails to adapt to altered field conditions) fails to account for modern multicultural learners who routinely exhibit multi-layered repertoires, contextual code-switching, and conscious reflexivity rather than static, unyielding dispositions.</li>
                <li><em>Deficit-Labeling Hazard:</em> In practical pedagogy, an uncritical adoption of habitus gives teachers a sophisticated fatalistic excuse to lower expectations, viewing working-class or minority learners as culturally incompatible with academic rigor.</li>
            </ul>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Symbolic Violence &amp; Misrecognition (Pierre Bourdieu &amp; Jean-Claude Passeron)</h4>
            <p>Symbolic violence denotes the tacit, non-physical form of domination exerted through the complicity and misrecognition of dominated agents. It occurs when arbitrary cultural meanings, linguistic standards, and hierarchies of ruling groups are successfully imposed and internalized as natural, universal, and objective orders of reality.</p>
            <p><strong>1. History &amp; The Empirical Anomaly:</strong> Developed alongside Passeron in <em>Reproduction in Education, Society and Culture</em> (1970/1977) and elaborated in <em>Pascalian Meditations</em> (1997/2000). Built to address a core political question: why do deeply unequal social hierarchies remain stable without constant physical force or overt totalitarian surveillance? Classical Marxism posited false consciousness imposed from above. Bourdieu recognized that dominated agents actively participate in their own subordination because the cognitive tools they use to evaluate the world are themselves structured by the relations of domination.</p>
            <p><strong>2. Theoretical Mechanics:</strong> Schools exercise <em>pedagogic authority</em> to impose a <em>cultural arbitrary</em> (ruling-class culture). Through <em>misrecognition (méconnaissance)</em>, unequal outcomes are treated not as the consequence of class-biased curricula, but as reflections of natural talent and moral effort. The process is somaticized through feelings of shame, inadequacy, and verbal hesitation.</p>
            <p><span class="audit-label-strength">3. Legitimate Diagnostic Strengths:</span> Explains how mass education neutralizes overt rebellion. Disadvantaged students who struggle with academic curricula internalize their exclusion as personal intellectual failure rather than structural sorting, preserving institutional legitimacy and converting class privilege into meritocratic achievement.</p>
            <p><span class="audit-label-critique">4. Forensic Audit (Contradictions, Empirical Limits &amp; Practical Hazards):</span></p>
            <ul>
                <li><em>The Rancière Critique (The Paternalism of 'Complicity'):</em> Philosopher Jacques Rancière demonstrated that Bourdieu's claim that the dominated are complicit in their subjugation is intellectually condescending. It frames working-class people as blind dupes who walk passively to their slaughter, unable to understand their oppression until an elite sociologist explains it to them. In reality, marginalized students and parents frequently see through institutional hypocrisy with immense clarity.</li>
                <li><em>Erasing Subcultural Dignity:</em> Subcultural studies demonstrate that working-class youth rarely internalize shame meekly; they mock scholastic pomposity, carve out autonomous cultural dignity, and consciously reject academic values.</li>
                <li><em>Pedagogical Paralysis:</em> If every assessment, objective test, and behavioral standard is branded symbolic violence, educators are left morally paralyzed, unable to correct errors, maintain productive order, or assess real learning.</li>
            </ul>
        </div>

        <h3 class="tradition-header">Sociolinguistic &amp; Resistance Paradigms</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Restricted vs. Elaborated Codes (Basil Bernstein)</h4>
            <p>Basil Bernstein's structural sociolinguistic framework differentiating speech forms: <em>restricted codes</em> (context-dependent, condensed syntax based on shared local assumptions) and <em>elaborated codes</em> (universalistic, explicit syntax orienting meaning toward abstract conceptualization).</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> School curricula, pedagogical transmission, and examinations operate almost exclusively through elaborated codes. Disadvantaged students, whose primary home socialization may center around communal restricted codes, face structural barriers not because their native language is deficient, but because schooling requires a culturally specific communicative orientation.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> William Labov and linguistic anthropologists demonstrated that working-class dialects possess rich grammatical complexity, logic, and abstract capacity. Bernstein was widely misconstrued by educational bureaucracies as endorsing a cultural deficit model, driving remedial tracks that degraded disadvantaged learners.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Counter-School Resistance (Paul Willis)</h4>
            <p>Paul Willis's ethnographic study (<em>Learning to Labour</em>, 1977) of working-class adolescent 'lads' constructing an anti-school subculture grounded in manual labor pride, physical solidarity, and opposition to institutional authority.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Directly countered Bourdieu's passive reproduction model by demonstrating agency. The lads saw through the meritocratic myth, correctly recognizing that hard academic work would not guarantee them middle-class parity.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Willis exposed a tragic paradox: the lads\' active, counter-hegemonic cultural resistance sealed their own educational failure, channeling them directly into the shop-floor exploitation they sought to validate. Furthermore, the subculture was steeped in virulent sexism, racism, and homophobia, complicating romanticized readings of anti-school resistance.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Social Closure &amp; Credentialism (Max Weber / Randall Collins)</h4>
            <p>Neo-Weberian sociology showing how dominant status groups use educational credentials as monopolistic gatekeeping currencies to restrict access to lucrative professional markets and maintain social boundaries.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Explains degree inflation. As higher education access expands, elite groups continually escalate baseline credential requirements (requiring postgraduate degrees, unpaid internships, or elite institutional pedigrees) to preserve exclusivity.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Functionalist and human capital models emphasize that modern economies genuinely require sophisticated technological, legal, and biomedical knowledge. Reducing all credentialing to predatory gatekeeping understates the genuine technical skill required in modern professions.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Residualisation</h4>
            <p>The structural decline of comprehensive public neighborhood schools caused by state subsidization of private education, selective school streaming, and middle-class flight from state schools.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Explains how marketized choice policies systematically peel affluent families and high-performing students away from local state schools, leaving them with concentrated disadvantage, complex developmental needs, and declining per-capita community resources.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Often deployed fatalistically by educational administrators to explain away institutional stagnation. Research indicates that high-quality leadership, explicit evidence-based instruction, and strong school culture can deliver exceptional outcomes even in highly residualised public settings.</p>
        </div>
    </section>

    <!-- 2. RACE, ETHNICITY & INDIGENEITY -->
    <section>
        <h2>2. Race, Ethnicity &amp; Indigeneity</h2>
        <h3 class="tradition-header">Postcolonial &amp; Critical Race Paradigms</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Colonisation of the Mind (Frantz Fanon)</h4>
            <p>Frantz Fanon's psychoanalytic postcolonial concept (<em>Black Skin, White Masks</em>, 1952) analyzing how imperial schooling operates as an apparatus of psychological subjugation, compelling colonized subjects to internalize perceived inferiority.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Highlights the destructive psychic consequences of assimilationist education, where First Nations and racialized learners are forced to abandon their native linguistic traditions, cultures, and cosmologies to measure their human worth against the colonizer's standard.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Over-emphasizing totalizing psychological damage can inadvertently portray Indigenous communities purely through victimhood and trauma narratives, obscuring enduring sovereign resilience, agency, and oral scholarship.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Epistemic Violence (Gayatri Spivak)</h4>
            <p>Gayatri Chakravorty Spivak's postcolonial formulation describing the institutional silencing, delegitimation, and destruction of subaltern knowledge traditions by dominant colonial epistemologies.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Unpacks how state curricula systematically treat Western Enlightenment epistemologies as universal rationality while categorizing Indigenous cosmologies as primitive folklore or decorative cultural artifacts.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> If pushed to radical extremes, epistemic critiques can drift into anti-scientific relativism, dismissing foundational universal sciences, empirical testing, and medicine as mere tools of colonial hegemony.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Institutional Racism &amp; Whiteness as Policy (David Gillborn)</h4>
            <p>Critical Race Theory (CRT) framework demonstrating that educational racism is not reducible to isolated interpersonal bigotry, but is embedded within routine institutional rules, funding formulas, streaming metrics, and assessment regimes.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Reveals how ostensibly race-neutral routines (e.g., behavioral discipline codes, tier-testing policies, gifted and talented matrices) systematically reproduce racial stratification and protect white majoritarian privilege.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Gillborn's thesis that education policy actively conspires to defend white supremacy can slip into conspiratorial cynicism, dismissing positive legislative reforms, anti-discrimination laws, and targeted equity funding as mere window dressing.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Culturally Sustaining Pedagogy (Django Paris / H. Samy Alim)</h4>
            <p>An equity framework requiring schools not merely to acknowledge minority cultural practices, but to actively sustain and revitalize linguistic, cultural, and community traditions as sovereign intellectual heritage.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Eliminates tokenistic multiculturalism, partnering with community Elders and embedding Indigenous epistemologies organically into curricular design.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Sustaining cultural vernaculars must not occur at the expense of mastering the dominant technical codes necessary for broader socioeconomic mobility. Equity requires balancing cultural sovereignty with uncompromising academic rigor.</p>
        </div>
    </section>

    <!-- 3. GENDER & SEXUALITIES -->
    <section>
        <h2>3. Gender &amp; Sexualities</h2>
        <h3 class="tradition-header">Structural Gender Orders &amp; Poststructuralist Performativity</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Gender Regimes &amp; Hegemonic Masculinity (Raewyn Connell)</h4>
            <p>Raewyn Connell's sociology of the gender order, describing an institutionalized power hierarchy with <em>hegemonic masculinity</em> at the apex—lionized through physical dominance, emotional detachment, and compulsory heterosexuality.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Analyzes schools as active factories of gender identity. Formal tracking, aggressive sports hierarchies, and playground peer policing systematically reward hegemonic conformity while punishing marginalized masculinities and non-conforming expressions.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Hegemonic masculinity can be deployed so broadly as to lose descriptive utility. Furthermore, male underachievement in literacy and educational completion requires concrete structural and developmental interventions, which pathologizing masculinity fails to address.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Gender Performativity (Judith Butler)</h4>
            <p>Judith Butler's poststructuralist thesis (<em>Gender Trouble</em>, 1990) that gender is not a stable biological reality, but a stylized repetition of bodily acts, linguistic codes, and regulatory citations maintained through ongoing surveillance.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Exposes how daily school rituals (gender-segregated lines, uniform policing, binary sports, administrative enrollment forms) continually re-inscribe the gender binary as an unassailable biological truth.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Butler's radical denial of biological materiality and reliance on opaque linguistic determinism clashes with developmental psychology and neurobiology, leaving educators without a practical framework for the physical developmental realities of puberty and adolescence.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Compulsory Heterosexuality (Adrienne Rich)</h4>
            <p>Adrienne Rich's feminist critique demonstrating that heterosexuality is an institutionalized political apparatus designed to enforce social conformity, female domestic subservience, and patriarchal stability.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Illuminates the pervasive heteronormative hidden curriculum of schools—prom events, literature canons, administrative forms, and staffroom discourse—which marginalizes LGBTQ+ identities.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Formulated in 1980, the theory struggles to capture the rapid, profound legal and cultural transformations of the 21st century, where affirmative policies and anti-discrimination frameworks have gained formal institutional grounding.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Minority Stress &amp; Affirmative Pedagogy</h4>
            <p>Public health and educational framework addressing the chronic, institutionalized psychological distress experienced by LGBTQ+ youth due to unsupportive climates, peer harassment, and school silence.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Mandates explicit institutional interventions: zero-tolerance bullying enforcement, inclusive health curricula, student privacy protections, and affirming pastoral support.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Affirmative pedagogy must balance pastoral sensitivity with statutory neutrality and parental engagement, avoiding institutional overreach that alienates families or polarizes communities.</p>
        </div>
    </section>

    <!-- 4. GOVERNANCE & SUBJECTIVITY -->
    <section>
        <h2>4. Governance, Surveillance &amp; Subjectivity</h2>
        <h3 class="tradition-header">The Foucaultian Architecture of Power</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Disciplinary Power &amp; Docile Bodies (Michel Foucault)</h4>
            <p>Michel Foucault's analysis (<em>Discipline and Punish</em>, 1975) of diffuse modern power that trains, optimizes, and coordinates the human body through meticulous spatial distribution, temporal routines, and continuous exercises.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Explains how classroom desks, timetable bells, uniform checks, and handwriting drills produce <em>docile bodies (corps dociles)</em>—individuals engineered for economic productivity while remaining politically obedient.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Foucault's reduction of all schooling to institutional subjugation ignores the emancipatory potential of discipline. Self-regulation, cognitive focus, and procedural routines are indispensable prerequisites for deep mathematical, artistic, and intellectual mastery.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">The Panopticon &amp; The Disciplinary Triad (Michel Foucault)</h4>
            <p>Bentham's architectural model adapted by Foucault, operating alongside the Disciplinary Triad: <em>hierarchical observation</em> (surveillance pyramids), <em>normalizing judgment</em> (penalizing deviations from an artificial norm), and <em>the examination</em> (quantifying and categorizing human subjects).</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Demonstrates how the unverifiable possibility of observation compels students to internalize surveillance, transforming coercion into autonomous self-policing. The examination transforms unique human beings into quantifiable administrative files.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Dismissing all diagnostic testing, assessment matrices, and behavioral norms as sinister panoptic surveillance leaves teachers unable to assess whether children can actually read, calculate, or safely cooperate in social spaces.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Governmentality &amp; Technologies of the Self (Michel Foucault)</h4>
            <p>Governing 'at a distance' by structuring the field of possible action, steering individuals to exercise their freedom in alignment with institutional and economic objectives.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Explains modern pastoral strategies (self-reflection rubrics, learning goals, mindfulness apps) that co-opt student interiority, training children to become self-auditing entrepreneurs of their own compliance.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Cynically recasting genuine student metacognition, self-reflection, and emotional regulation purely as insidious state manipulation deprives students of essential tools for self-improvement and resilience.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">The Psy-Complex &amp; Medicalisation of Deviance (Nikolas Rose / Peter Conrad)</h4>
            <p>Nikolas Rose's analysis of psychological regulatory networks, combined with Peter Conrad's thesis that non-compliant behaviors are increasingly redefined as clinical psychiatric pathologies (e.g., ADHD, ODD).</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Highlights how schools depoliticize institutional tensions—such as rigid scheduling or unengaging curricula—by attributing student restlessness to individual chemical imbalances, absolving the school of reform.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Denying neurodevelopmental reality harms students who legitimately suffer from neurodivergence and benefit greatly from clinical support, therapeutic intervention, and assistive education plans.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Digital Panopticon &amp; Dataveillance</h4>
            <p>Ubiquitous algorithmic architectures (LMS telemetry, ClassDojo, biometric scanning) tracking real-time student activity across physical and digital school spaces.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Exposes how digital platforms extend institutional surveillance into domestic spaces, conditioning youth to accept permanent algorithmic surveillance as natural.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Fails to acknowledge the pedagogical necessity of learning analytics in identifying learning gaps, automating grading workloads, and safeguarding vulnerable children online.</p>
        </div>
    </section>

    <!-- 5. NEOLIBERALISM & DATAFICATION -->
    <section>
        <h2>5. Neoliberalism &amp; Datafication</h2>
        <h3 class="tradition-header">Marketization, Managerialism &amp; Platform Capitalism</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Performativity &amp; Audit Culture (Stephen Ball)</h4>
            <p>Stephen Ball's critique of neoliberal education policy, where professional trust is replaced by corporate managerialism, key performance indicators (KPIs), public rankings, and incessant data auditing.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Diagnoses how public league tables and audit pressures compel schools to practice fabrication—narrowing the curriculum to test drills, gaming attendance data, and subordinating pedagogy to public metrics.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Completely abandoning performance transparency risks entrenching educational mediocrity, shielding underperforming institutions from accountability to the public and disadvantaged communities.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Horizontal Competition</h4>
            <p>Zero-sum market competition between schools operating at the same tier within a regional catchment for student enrollment and associated voucher funding.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Demonstrates how market competition diverts school budgets into glossy branding, while incentivizing institutions to 'cream-skim' high-achieving students and subtly shed students with complex learning needs.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Total elimination of school choice can lock disadvantaged families into historically underperforming neighborhood schools with no structural exit mechanism.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Governance by Numbers &amp; Accountability Washback (Bob Lingard)</h4>
            <p>Bob Lingard's framework describing how the state steers education systems remotely through centralized census testing data, producing severe pedagogical washback.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Explains how high-stakes census testing (e.g., NAPLAN) leads to curriculum distortion, the unethical triage of 'bubble' students near reporting thresholds, and the abandonment of arts and humanities.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Objective, standardized baseline data is vital for identifying macroscopic literacy gaps and directing targeted equity funding to under-resourced public school sectors.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Surveillance Capitalism (Shoshana Zuboff)</h4>
            <p>Shoshana Zuboff's economic framework describing how commercial digital tech monopolies extract student behavioral surplus as proprietary data for predictive behavioral modification and profit.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Highlights the predatory enclosure of public educational infrastructure by commercial EdTech platforms, harvesting student behavioral analytics while bypassing privacy protections.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Conflating commercial platform capitalism with all educational technology obscures how well-governed, non-profit digital learning platforms can expand educational access in remote communities.</p>
        </div>
    </section>

    <!-- 6. CULTURE & TECHNOLOGY -->
    <section>
        <h2>6. Culture &amp; Technology</h2>
        <h3 class="tradition-header">Media Studies, Subcultural Agency &amp; Cognitive Ecology</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Active Audience Theory &amp; Polysemy (Stuart Hall)</h4>
            <p>Stuart Hall's encoding/decoding model demonstrating that media texts are polysemic (bearing multiple interpretations) and actively negotiated by audiences through dominant, negotiated, or oppositional stances.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Refutes paternalistic views that school students are passive victims brainwashed by screen media, highlighting their capacity to critically evaluate, mock, and subvert cultural messaging.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Hall's theory can lead educators to underestimate the coercive algorithmic engineering of modern social feeds, which exploit neurological dopamine loops far beyond active intellectual negotiation.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Semiotic Democracy &amp; Textual Poaching (John Fiske)</h4>
            <p>John Fiske's concept that youth audiences actively seize corporate cultural products (memes, fashion, video games), remixing and subverting corporate signs to construct autonomous meaning.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Validates youth cultural creativity against Frankfurt School pessimism, showing how youth resist cultural homogenization.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Often drifts into romanticized populism, confusing trivial consumer customization (e.g., creating TikTok memes) with substantive political emancipation or critical intellectual work.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Intertextuality &amp; Moral Panics (Julia Kristeva / Stanley Cohen)</h4>
            <p>Kristeva's textual mosaic concept alongside Cohen's sociological model of media-manufactured societal panics framing youth behaviors or educational standards as existential threats.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Unmasks how sensationalist media cycles manufacture synthetic educational crises to justify draconian disciplinary crackdowns and curriculum censorship.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Dismissing all legitimate community anxieties regarding youth mental health, screen addiction, or declining national literacy metrics as manufactured panics avoids addressing real educational decline.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Media Ecology &amp; The Social Model of Disability (Neil Postman / Mike Oliver)</h4>
            <p>Postman's Faustian analysis of technological trade-offs paired with Oliver's social model defining disability as an institutional mismatch with inaccessible environments.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Identifies the cognitive costs of digital fragmentation while championing Universal Design for Learning (UDL) and assistive technologies to eliminate institutional classroom barriers.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Extreme social model assertions risk minimizing the painful, biological realities of physical or neurocognitive impairments that require specialized medical and developmental support.</p>
        </div>
    </section>

    <!-- 7. PHILOSOPHY, LAW & RIGHTS -->
    <section>
        <h2>7. Philosophy, Law &amp; Educational Rights</h2>
        <h3 class="tradition-header">Critical Praxis, Ethics &amp; Jurisprudence</h3>

        <div class="forensic-entry">
            <h4 class="concept-title">Critical Pedagogy &amp; Praxis (Paulo Freire)</h4>
            <p>Paulo Freire's critique (<em>Pedagogy of the Oppressed</em>, 1968) of the 'banking model' of education in favor of problem-posing dialogue, conscientisation (critical consciousness), and praxis (uniting reflection and action for liberation).</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Challenges authoritarian rote learning, elevating education into a collaborative project where learners interrogate real-world oppression and democratize classroom power relations.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Cognitive load research consistently demonstrates that novice learners, particularly from disadvantaged backgrounds, suffer under unstructured discovery learning and require explicit, structured instruction. Furthermore, Freirean pedagogy can degenerate into ideological indoctrination where political activism displaces academic mastery.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Normative Ethics &amp; Relational Care (Nel Noddings / Aristotle)</h4>
            <p>The philosophical synthesis of Kantian deontology (treating learners as ends, never as means), Aristotelian phronesis (practical wisdom), and Nel Noddings' ethics of care grounded in attentiveness and trust.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Forbids the instrumental use of children as data points for league tables, demanding that teachers anchor their professional duty in empathy and pastoral responsiveness.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> An uncritical ethics of care can lead to sentimentalism, conflating care with lowering academic expectations or avoiding necessary disciplinary boundaries and challenging curricula.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Non-Delegable Duty of Care &amp; Negligence</h4>
            <p>The common law tort doctrine imposing an affirmative, non-delegable duty upon schools and teachers to take reasonable precautions against foreseeable risks of physical and psychiatric harm.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Establishes the legal floor of the profession, demanding vigilant supervision across classrooms, playgrounds, and excursions to protect student safety.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Defensive risk aversion driven by tort liability can lead to hyper-sanitized educational environments that ban beneficial physical play, challenging scientific experiments, and outdoor exploration.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">UNCRC Article 12 &amp; Participatory Rights</h4>
            <p>The United Nations Convention on the Rights of the Child (1989), specifically Article 12 guaranteeing children the right to express their views freely in all matters affecting them.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Disrupts institutional paternalism by mandating authentic student participation in pedagogical decisions, disciplinary hearings, and school governance.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Participatory rights are frequently hollowed out into tokenistic student councils, or misconstrued by progressive reformers as conferring equal authority to novice children over expert curriculum content.</p>
        </div>

        <div class="forensic-entry">
            <h4 class="concept-title">Regimes of Truth vs. Powerful Knowledge (Michel Foucault / Michael Young)</h4>
            <p>The intellectual tension between Foucault's poststructuralist assertion that all knowledge is a power-laden 'regime of truth,' and Michael Young's Social Realism defending universal access to 'powerful knowledge'—specialized, discipline-grounded knowledge.</p>
            <p><strong>1. Mechanics &amp; Strengths:</strong> Foucault exposes curriculum bias, while Young demonstrates that specialized disciplinary knowledge (science, history, mathematics) takes students beyond their localized personal experiences, enabling them to understand and transform the world.</p>
            <p><span class="audit-label-critique">2. Forensic Audit:</span> Postmodern rejection of disciplinary knowledge under the banner of fighting hegemonic truth disproportionately damages working-class students, denying them the intellectual tools needed for higher education and democratic agency.</p>
        </div>
    </section>

    <!-- FORMAL BIBLIOGRAPHY -->
    <section class="biblio-section">
        <h2>Primary Sources &amp; Critical References</h2>
        <ul class="biblio-list">
            <li><strong>Bourdieu, P. (1973).</strong> 'Cultural Reproduction and Social Reproduction'. In R. Brown (Ed.), <em>Knowledge, Education, and Cultural Change: Papers in the Sociology of Education</em> (pp. 71–112). London: Tavistock Publications.</li>
            <li><strong>Bourdieu, P. (1977).</strong> <em>Outline of a Theory of Practice</em> (R. Nice, Trans.). Cambridge: Cambridge University Press. (Original work published in French 1972).</li>
            <li><strong>Bourdieu, P. (1984).</strong> <em>Distinction: A Social Critique of the Judgement of Taste</em> (R. Nice, Trans.). Cambridge, MA: Harvard University Press. (Original work published in French 1979).</li>
            <li><strong>Bourdieu, P. (1986).</strong> 'The Forms of Capital'. In J. G. Richardson (Ed.), <em>Handbook of Theory and Research for the Sociology of Education</em> (pp. 241–258). New York: Greenwood Press.</li>
            <li><strong>Bourdieu, P., &amp; Passeron, J.-C. (1977).</strong> <em>Reproduction in Education, Society and Culture</em> (R. Nice, Trans.). London: Sage Publications. (Original work published in French 1970).</li>
            <li><strong>Collins, R. (1979).</strong> <em>The Credential Society: An Historical Sociology of Education and Stratification</em>. New York: Academic Press.</li>
            <li><strong>Delpit, L. (1988).</strong> 'The Silenced Dialogue: Power and Pedagogy in Educating Other People's Children'. <em>Harvard Educational Review</em>, 58(3), 280–298.</li>
            <li><strong>Fanon, F. (1967).</strong> <em>Black Skin, White Masks</em> (C. L. Markmann, Trans.). New York: Grove Press. (Original work published in French 1952).</li>
            <li><strong>Foucault, M. (1977).</strong> <em>Discipline and Punish: The Birth of the Prison</em> (A. Sheridan, Trans.). London: Allen Lane. (Original work published in French 1975).</li>
            <li><strong>Freire, P. (1970).</strong> <em>Pedagogy of the Oppressed</em> (M. B. Ramos, Trans.). New York: Herder and Herder. (Original work published in Portuguese 1968).</li>
            <li><strong>Rancière, J. (2003).</strong> <em>The Philosopher and His Poor</em> (J. Drury, C. Oster, &amp; A. Parker, Trans.). Durham, NC: Duke University Press. (Original work published in French 1983).</li>
            <li><strong>Willis, P. (1977).</strong> <em>Learning to Labour: How Working Class Kids Get Working Class Jobs</em>. Farnborough: Saxon House.</li>
            <li><strong>Young, M. (2008).</strong> <em>Bringing Knowledge Back In: From Social Constructivism to Social Realism in the Sociology of Education</em>. London: Routledge.</li>
        </ul>
    </section>

    <a href="index.html" class="back-link">&larr; Return to Main Exam Revision Guide</a>

</body>
</html>
'''
    return template


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
    print(f"Successfully deployed bulletproof Cultural Capital dossier to: {target_file.resolve()}")

    commit_message = (
        "Upgrade Cultural Capital dossier with exact primary mechanics and bibliography\n\n"
        "Enhance the Cultural Capital entry in core-concepts.html with primary\n"
        "mechanisms from Bourdieu's texts: the economy of acquisition time, the\n"
        "intraclass teacher-vs-capitalist divide, legitimate autodidacticism, and\n"
        "credential devaluation. Append an authoritative academic bibliography.\n\n"
        "- Add labor-time economy and 'wasted time' mechanics from 1986 text.\n"
        "- Detail the structural split between cultural and economic elites.\n"
        "- Explain the devaluation of scholastic pedantry vs. natural ease.\n"
        "- Append a primary and critical counterweight bibliography."
    )

    sync_repository(root_directory, commit_message)


if __name__ == "__main__":
    main()
