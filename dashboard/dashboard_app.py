from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from dataclasses import asdict

from app.parser.tree_parser import parse_file
from app.agents.security import run_security_agent
from app.agents.logic import run_logic_agent
from app.agents.style import run_style_agent
from app.reviewer.aggregator import aggregate_findings
from app.reviewer.formatter import format_review_markdown

st.set_page_config(page_title="AI Code Review Dashboard", layout="wide")
st.title("AI Code Review Dashboard")
st.markdown(
    "A simple dashboard showing the current AI review pipeline results for sample code."
)

fixture_path = Path("tests/fixtures/sql_injection.py")
content = fixture_path.read_text(encoding="utf-8")
code_facts = parse_file(str(fixture_path), content, [])

security_findings = run_security_agent(content)
logic_findings = run_logic_agent(content)
style_findings = run_style_agent(content)

findings = [asdict(f) for f in security_findings + logic_findings + style_findings]
review = aggregate_findings(findings)
formatted_review = format_review_markdown(review)

severity_counts = {
    "HIGH": sum(1 for f in findings if f.get("severity") == "HIGH"),
    "MEDIUM": sum(1 for f in findings if f.get("severity") == "MEDIUM"),
    "LOW": sum(1 for f in findings if f.get("severity") == "LOW"),
}

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Findings", len(findings))
col2.metric("High Severity", severity_counts["HIGH"])
col3.metric("Medium Severity", severity_counts["MEDIUM"])
col4.metric("Low Severity", severity_counts["LOW"])

st.markdown("---")
st.subheader("Review Summary")
st.info(f"{review.get('summary', 'No summary available')} \n\nReviewed file: `{fixture_path}`")

st.markdown("### Findings")
for idx, finding in enumerate(review["findings"], start=1):
    with st.expander(f"{idx}. {finding.get('severity', 'INFO')} — {finding.get('category', 'General')}"):
        st.write(f"**Message:** {finding.get('message', '')}")
        st.write(f"**Suggestion:** {finding.get('suggestion', '')}")
        st.write(f"**Agent:** {finding.get('agent_name', '')}")
        if finding.get("file_path"):
            st.write(f"**File:** {finding.get('file_path')}")
        if finding.get("line_start") or finding.get("line_end"):
            st.write(
                f"**Location:** {finding.get('line_start', 0)}-{finding.get('line_end', 0)}"
            )

st.markdown("---")
st.markdown("### Formatted Review")
st.code(formatted_review, language="markdown")
