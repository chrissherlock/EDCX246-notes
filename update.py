#!/usr/bin/env python3
"""Restore complete card styling across all module pages while refining

only the in-page Table of Contents into a lightweight typographic directory.
"""

from pathlib import Path
import re
import subprocess
import sys

STANDARD_STYLE_BLOCK = """        :root {
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
            align-items: flex-start;
            gap: 18px;
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--primary);
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 24px;
        }
        .intro-card p {
            margin: 0;
            font-size: 0.92rem;
            color: #44403c;
            line-height: 1.6;
            text-align: justify;
        }

        /* Lightweight Typographic Table of Contents */
        .toc-card {
            background-color: var(--bg-banner);
            border: 1px solid #fed7aa;
            border-left: 3px solid var(--primary);
            border-radius: 6px;
            padding: 14px 18px 16px 18px;
            margin: 20px 0 28px 0;
        }
        .toc-header-row {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px dashed #fed7aa;
        }
        .toc-card h3 {
            font-size: 0.82rem;
            color: var(--primary-dark);
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
        }
        .toc-badge {
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .toc-grid {
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 6px 20px;
        }
        .toc-grid li {
            margin: 0;
            padding: 0;
        }
        .toc-grid a {
            display: flex;
            align-items: baseline;
            gap: 8px;
            padding: 3px 0;
            color: var(--text-main);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 500;
            transition: color 0.15s ease-in-out;
        }
        .toc-index {
            font-size: 0.74rem;
            font-weight: 700;
            color: var(--primary);
            opacity: 0.8;
            font-variant-numeric: tabular-nums;
            flex-shrink: 0;
        }
        .toc-item-label {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .toc-chevron {
            display: none;
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
        .diagram-container, .counter-svg-container {
            margin: 16px 0;
            text-align: center;
        }
        .diagram-container svg, .counter-svg-container svg {
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }
        .counter-tradition-box {
            margin-top: 18px;
            padding: 16px 18px;
            background-color: #ffffff;
            border: 1px solid #fed7aa;
            border-left: 4px solid var(--accent-orange);
            border-radius: 6px;
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
        .module-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: 20px 0;
            padding: 10px 0;
            border-top: 1px solid var(--border-subtle, #e7e5e4);
            border-bottom: 1px solid var(--border-subtle, #e7e5e4);
        }
        .nav-btn {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            background-color: var(--bg-banner, #fffbf5);
            border: 1px solid var(--border-accent, #f59e0b);
            border-radius: 6px;
            color: var(--primary-dark, #78350f);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 600;
            transition: background-color 0.15s ease-in-out, color 0.15s ease-in-out;
        }
        .nav-btn:hover {
            background-color: var(--primary, #b45309);
            color: #ffffff;
            border-color: var(--primary, #b45309);
        }
        .nav-btn.disabled {
            opacity: 0.4;
            pointer-events: none;
            cursor: default;
            border-color: var(--border-subtle, #e7e5e4);
        }
        @media (max-width: 768px) {
            .camp-cards { grid-template-columns: 1fr; }
        }
"""


def restore_pages(root_dir: Path) -> None:
    targets = [root_dir / f"module-{i}.html" for i in range(1, 8)]

    for path in targets:
        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")

        # Replace the entire <style>...</style> block with the restored standard styles
        content = re.sub(
            r"<style>.*?</style>",
            f"<style>\n{STANDARD_STYLE_BLOCK}    </style>",
            content,
            flags=re.DOTALL,
        )

        path.write_text(content, encoding="utf-8")
        print(f"Restored complete card styling in {path.name}")


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
    restore_pages(root_directory)

    commit_message = (
        "Revert page card styling while preserving clean TOC directory\n\n"
        "Restore full forensic container, scenario, and counter-tradition\n"
        "card styles across all module pages while retaining lightweight\n"
        "typographic directory formatting for Table of Contents."
    )

    sync_repository(repo_path=root_directory, commit_msg=commit_message)


if __name__ == "__main__":
    main()
