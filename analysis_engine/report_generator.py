import html
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from backend.config import INSTITUTION_NAME, INSTITUTION_CAMPUS, INSTITUTION_DEPT, REPORTS_DIR

class ReportGenerator:
    """
    Generates standalone, print-ready and beautifully styled HTML plagiarism reports.
    """

    @classmethod
    def generate_html_report(
        cls,
        scan_data: Dict[str, Any],
        student_info: Dict[str, Any],
        comparison_matches: List[Dict[str, Any]],
        ai_details: Dict[str, Any]
    ) -> str:
        timestamp_str = datetime.utcnow().strftime("%B %d, %Y - %H:%M:%S UTC")
        overall_score = scan_data.get("overall_similarity", 0.0)
        risk_level = scan_data.get("risk_level", "Low")
        ai_score = scan_data.get("ai_pattern_score", 0.0)

        # Risk badge color
        if risk_level == "Critical":
            risk_color = "#DC2626"
            risk_bg = "#FEE2E2"
        elif risk_level == "High":
            risk_color = "#EA580C"
            risk_bg = "#FFEDD5"
        elif risk_level == "Moderate":
            risk_color = "#D97706"
            risk_bg = "#FEF3C7"
        else:
            risk_color = "#16A34A"
            risk_bg = "#DCFCE7"

        # AI badge color
        if ai_score >= 60:
            ai_color = "#DC2626"
            ai_bg = "#FEE2E2"
        elif ai_score >= 30:
            ai_color = "#D97706"
            ai_bg = "#FEF3C7"
        else:
            ai_color = "#16A34A"
            ai_bg = "#DCFCE7"

        # Matches HTML
        matches_html = ""
        for idx, match in enumerate(comparison_matches[:5], 1):
            sub_b = match.get("submission_b", {})
            m_score = match.get("similarity_score", 0.0)
            m_blocks = match.get("matching_blocks", [])

            blocks_html = ""
            for b in m_blocks[:4]:
                snippet_a = html.escape(b.get("snippet_a", ""))
                snippet_b = html.escape(b.get("snippet_b", ""))
                blocks_html += f"""
                <div class="block-card">
                    <div class="block-header">
                        <span class="badge">{b.get('block_type', 'Matched Block')}</span>
                        <span>Source A (L{b.get('start_a')}-L{b.get('end_a')}) &harr; Source B (L{b.get('start_b')}-L{b.get('end_b')})</span>
                        <span class="block-sim">{b.get('similarity', 0)}% Similarity</span>
                    </div>
                    <div class="code-compare-grid">
                        <div class="code-box">
                            <div class="code-title">Target Student Snippet</div>
                            <pre><code>{snippet_a}</code></pre>
                        </div>
                        <div class="code-box">
                            <div class="code-title">Matched Peer Snippet</div>
                            <pre><code>{snippet_b}</code></pre>
                        </div>
                    </div>
                </div>
                """

            matches_html += f"""
            <div class="match-item">
                <div class="match-summary">
                    <div>
                        <h4 style="margin:0; font-size:1.05rem; color:#0F172A;">Match #{idx}: {html.escape(sub_b.get('student_name', 'Student'))} ({html.escape(sub_b.get('matric_number', 'N/A'))})</h4>
                        <div style="font-size:0.85rem; color:#64748B; margin-top:3px;">File: {html.escape(sub_b.get('file_name', 'code'))} | Course: {html.escape(student_info.get('course_code', 'N/A'))}</div>
                    </div>
                    <div class="match-score-badge" style="font-size:1.2rem; font-weight:700; color:{risk_color};">
                        {m_score}% Match
                    </div>
                </div>
                <div class="metrics-row" style="margin: 12px 0;">
                    <span class="pill">AST: {match.get('ast_similarity', 0)}%</span>
                    <span class="pill">Token: {match.get('token_similarity', 0)}%</span>
                    <span class="pill">Fingerprint: {match.get('fingerprint_similarity', 0)}%</span>
                    <span class="pill">Normalized: {match.get('normalized_similarity', 0)}%</span>
                </div>
                {blocks_html}
            </div>
            """

        if not matches_html:
            matches_html = "<p style='color:#64748B; font-style:italic;'>No significant repository matches detected.</p>"

        # AI Indicators HTML
        ai_indicators = ai_details.get("indicators", [])
        ai_indicators_html = "".join([f"<li>{html.escape(ind)}</li>" for ind in ai_indicators])

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COOUCodeGuard Analysis Report - Scan #{scan_data.get('id')}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #0F172A;
            background: #F8FAFC;
            padding: 30px 20px;
            line-height: 1.5;
        }}
        .report-container {{
            max-width: 960px;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid #E2E8F0;
        }}
        .header {{
            border-bottom: 2px solid #2563EB;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        .institution-title {{
            font-size: 1.35rem;
            font-weight: 800;
            color: #1E3A8A;
            letter-spacing: -0.02em;
        }}
        .institution-sub {{
            font-size: 0.9rem;
            color: #475569;
            font-weight: 500;
            margin-top: 2px;
        }}
        .system-badge {{
            background: #EFF6FF;
            color: #2563EB;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            border: 1px solid #BFDBFE;
            text-align: right;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .meta-card {{
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 16px 20px;
        }}
        .meta-card h3 {{
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
            margin-bottom: 10px;
        }}
        .meta-row {{
            display: flex;
            justify-content: space-between;
            padding: 4px 0;
            font-size: 0.9rem;
        }}
        .meta-label {{ color: #64748B; font-weight: 500; }}
        .meta-val {{ font-weight: 600; color: #0F172A; }}
        .score-hero {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .score-card {{
            flex: 1;
            padding: 24px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #E2E8F0;
        }}
        .score-num {{
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 8px 0;
        }}
        .score-desc {{
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .breakdown-bar {{
            display: flex;
            gap: 12px;
            margin-top: 15px;
        }}
        .pill {{
            background: #F1F5F9;
            color: #334155;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid #CBD5E1;
        }}
        .section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #1E293B;
            margin: 30px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid #E2E8F0;
        }}
        .match-item {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 16px;
        }}
        .match-summary {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .code-compare-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 10px;
        }}
        .code-box {{
            background: #0F172A;
            color: #F8FAFC;
            border-radius: 6px;
            padding: 12px;
            font-size: 0.8rem;
            overflow-x: auto;
        }}
        .code-title {{
            color: #94A3B8;
            font-size: 0.75rem;
            margin-bottom: 6px;
            text-transform: uppercase;
            font-weight: 600;
        }}
        pre {{ margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
        .badge {{
            background: #EFF6FF;
            color: #1D4ED8;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
        }}
        .block-card {{
            margin-top: 12px;
            padding: 12px;
            background: #F8FAFC;
            border-radius: 6px;
            border: 1px solid #E2E8F0;
        }}
        .block-header {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #475569;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .disclaimer-box {{
            margin-top: 40px;
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-radius: 8px;
            padding: 16px 20px;
            font-size: 0.85rem;
            color: #92400E;
        }}
        .disclaimer-box strong {{
            display: block;
            margin-bottom: 4px;
            color: #78350F;
        }}
        .no-print {{
            margin-bottom: 20px;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }}
        .print-btn {{
            background: #2563EB;
            color: #FFFFFF;
            border: none;
            padding: 10px 18px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
        }}
        @media print {{
            body {{ background: #FFFFFF; padding: 0; }}
            .report-container {{ border: none; box-shadow: none; padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="no-print">
            <button class="print-btn" onclick="window.print()">Print / Save as PDF</button>
        </div>

        <header class="header">
            <div>
                <div class="institution-title">{INSTITUTION_NAME}</div>
                <div class="institution-sub">{INSTITUTION_CAMPUS} &bull; {INSTITUTION_DEPT}</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">Official Source Code Plagiarism &amp; AI Pattern Audit Report</div>
            </div>
            <div class="system-badge">
                COOUCodeGuard<br>
                <span style="font-size:0.75rem; font-weight:normal; color:#64748B;">Offline Engine v1.0</span>
            </div>
        </header>

        <div class="grid-2">
            <div class="meta-card">
                <h3>Submission Information</h3>
                <div class="meta-row"><span class="meta-label">Student Name:</span><span class="meta-val">{html.escape(student_info.get('student_name', 'N/A'))}</span></div>
                <div class="meta-row"><span class="meta-label">Matric Number:</span><span class="meta-val">{html.escape(student_info.get('matric_number', 'N/A'))}</span></div>
                <div class="meta-row"><span class="meta-label">Course:</span><span class="meta-val">{html.escape(student_info.get('course_code', 'N/A'))}</span></div>
                <div class="meta-row"><span class="meta-label">Assignment:</span><span class="meta-val">{html.escape(student_info.get('assignment_title', 'N/A'))}</span></div>
            </div>
            <div class="meta-card">
                <h3>Scan Audit Metadata</h3>
                <div class="meta-row"><span class="meta-label">Scan ID:</span><span class="meta-val">#{scan_data.get('id')}</span></div>
                <div class="meta-row"><span class="meta-label">Language:</span><span class="meta-val">{html.escape(student_info.get('language', 'N/A'))}</span></div>
                <div class="meta-row"><span class="meta-label">File Name:</span><span class="meta-val">{html.escape(student_info.get('file_name', 'N/A'))}</span></div>
                <div class="meta-row"><span class="meta-label">Timestamp:</span><span class="meta-val">{timestamp_str}</span></div>
            </div>
        </div>

        <div class="score-hero">
            <div class="score-card" style="background:{risk_bg}; border-color:{risk_color}40;">
                <div class="score-desc" style="color:{risk_color};">Overall Plagiarism Similarity</div>
                <div class="score-num" style="color:{risk_color};">{overall_score}%</div>
                <div style="font-weight:700; color:{risk_color}; font-size:1rem;">{risk_level} Risk Level</div>
                <div class="breakdown-bar" style="justify-content:center;">
                    <span class="pill">AST: {scan_data.get('ast_similarity', 0)}%</span>
                    <span class="pill">Token: {scan_data.get('token_similarity', 0)}%</span>
                    <span class="pill">Fingerprint: {scan_data.get('fingerprint_similarity', 0)}%</span>
                    <span class="pill">Text: {scan_data.get('normalized_similarity', 0)}%</span>
                </div>
            </div>

            <div class="score-card" style="background:{ai_bg}; border-color:{ai_color}40;">
                <div class="score-desc" style="color:{ai_color};">AI-Generated Code Indicator</div>
                <div class="score-num" style="color:{ai_color};">{ai_score}%</div>
                <div style="font-weight:700; color:{ai_color}; font-size:1rem;">{ai_details.get('classification', 'Low indication')}</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:8px;">Heuristic Boilerplate &amp; Pattern Score</div>
            </div>
        </div>

        <div class="section-title">AI Pattern Heuristics Analysis</div>
        <div class="meta-card">
            <ul style="padding-left: 20px; font-size: 0.9rem; color: #334155; line-height: 1.6;">
                {ai_indicators_html}
            </ul>
        </div>

        <div class="section-title">Top Peer Matches in Repository</div>
        {matches_html}

        <div class="section-title">Methodology &amp; Architecture</div>
        <div style="font-size:0.85rem; color:#475569; line-height:1.6;">
            COOUCodeGuard implements multi-stage offline code analysis combining Abstract Syntax Tree (AST) structural invariant extraction (45%), Token sequence normalization (25%), Winnowing k-gram min-hash fingerprinting (20%), and Normalized text sequence alignment (10%). All calculations occur exclusively on the local machine without cloud exposure.
        </div>

        <div class="disclaimer-box">
            <strong>Academic Review Notice &amp; Disclaimer:</strong>
            Similarity metrics and AI pattern detection scores produced by COOUCodeGuard are statistical heuristic indicators intended to guide academic review by departmental lecturers. They do not automatically constitute conclusive proof of academic dishonesty. Final decisions remain strictly the prerogative of the course lecturer and the departmental academic integrity board.
        </div>
    </div>
</body>
</html>"""
        return html_content

    @classmethod
    def save_report_file(cls, scan_id: int, html_content: str) -> Path:
        file_path = REPORTS_DIR / f"report_scan_{scan_id}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return file_path
