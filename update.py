#!/usr/bin/env python3
import sys
import re

def update_html_file(filename="index.html"):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            html = file.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found in the current directory.")
        sys.exit(1)

    # 1. Update Title and H1
    html = html.replace(
        "<title>EDCX246 Exam Revision Guide: Society and Education</title>",
        "<title>EDCX246 — Critical Engagement & Professional Synthesis</title>"
    )
    html = html.replace(
        "<h1>EDCX246 Exam Revision Guide: Society and Education</h1>",
        "<h1>EDCX246 Critical Engagement & Professional Synthesis</h1>"
    )

    # 2. Update the 4-Part Evaluation Framework Headers
    html = html.replace(
        "<strong>1. Strengths of the Argument (Thesis)</strong>",
        "<strong>1. Diagnostic Adequacy (The Sociological Lens)</strong>"
    )
    html = html.replace(
        "<strong>2. Inaccuracies &amp; Critique (Antithesis)</strong>",
        "<strong>2. Explanatory Boundaries (Methodological Overreach)</strong>"
    )
    html = html.replace(
        "<strong>3. Balanced Judgement (Synthesis)</strong>",
        "<strong>3. Epistemic Synthesis</strong>"
    )
    html = html.replace(
        "<strong>4. Pedagogical Conclusion (Application)</strong>",
        "<strong>4. Pedagogical Translation (Professional Practice)</strong>"
    )

    # 3. Reframe the Fundamental Problems Section Title
    html = html.replace(
        '<h2 id="fundamental-problems">Fundamental Problems &amp; Theoretical Blind Spots of the Text</h2>',
        '<h2 id="fundamental-problems">Critical Questions & Explanatory Boundaries</h2>'
    )

    # 4. Update the Table of Contents (Column 6)
    html = html.replace(
        '<span class="toc-column-title">6. Exam Practice &amp; Critique</span>',
        '<span class="toc-column-title">6. Professional Synthesis</span>'
    )
    html = html.replace(
        '<li><a href="#exam-notes-extension">2-Mark Scoring Strategy</a></li>',
        '<li><a href="#exam-notes-extension">Strategic Exam Deployment</a></li>'
    )
    html = html.replace(
        '<li><a href="#exam-notes-extension">High-Yield Practice Exam Bank</a></li>',
        '<li><a href="#exam-notes-extension">Applied Practice Scenarios</a></li>'
    )
    html = html.replace(
        '<li><a href="#exam-notes-extension">MCQ Elimination Rules</a></li>',
        '<li><a href="#exam-notes-extension">MCQ Epistemic Filtering</a></li>'
    )
    html = html.replace(
        '<li><a href="#fundamental-problems">7 Fundamental Blind Spots</a></li>',
        '<li><a href="#fundamental-problems">7 Critical Explanatory Boundaries</a></li>'
    )

    # 5. Insert the Site Methodology Disclaimer
    disclaimer_anchor = "populations.\n            </p>"
    disclaimer_html = """populations.
            </p>
            <div class="paradox-box" style="border-left-color: #2563eb; background-color: #eff6ff; margin: 20px 0;">
                <h4 style="color: #1e40af;">Site Methodology & Purpose</h4>
                <p style="color: #1e293b;">
                    This portal operates as a critical reading apparatus. It distinguishes between the <em>diagnostic adequacy</em> of the textbook's critical sociology (its ability to identify institutional sorting mechanisms) and its <em>explanatory boundaries</em>. By identifying where sociological critique risks overwriting developmental biology, cognitive science, and the informational necessity of explicit instruction, this guide translates course theory into rigorous, balanced professional practice.
                </p>
            </div>"""

    # Only insert if it hasn't been added yet
    if "Site Methodology & Purpose" not in html and disclaimer_anchor in html:
        html = html.replace(disclaimer_anchor, disclaimer_html, 1)

    # Write changes back to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html)

    print(f"Success: {filename} has been updated with the professional synthesis framework.")

if __name__ == "__main__":
    update_html_file()
