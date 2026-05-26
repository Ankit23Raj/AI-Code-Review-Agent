from pathlib import Path
import sys
from dataclasses import asdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import streamlit as st

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

if "review_data" not in st.session_state:
    st.session_state.review_data = None

if st.button("Run Review"):
    with st.spinner("Running AI review..."):
        fixture_path = Path("tests/fixtures/sql_injection.py")

        if not fixture_path.exists():
            st.error(f"Fixture file not found: {fixture_path}")
            st.stop()

        content = fixture_path.read_text(encoding="utf-8")
        code_facts = parse_file(str(fixture_path), content, [])

        security_findings = run_security_agent(content)
        logic_findings = run_logic_agent(content)
        style_findings = run_style_agent(content)

        findings = [asdict(f) for f in security_findings + logic_findings + style_findings]
        review = aggregate_findings(findings)
        formatted_review = format_review_markdown(review)

        st.session_state.review_data = {
            "fixture_path": str(fixture_path),
            "code_facts": code_facts,
            "findings": findings,
            "review": review,
            "formatted_review": formatted_review,
        }

        st.success("Review complete!")

if st.session_state.review_data:
    data = st.session_state.review_data
    findings = data["findings"]
    review = data["review"]

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Findings", len(findings))
    col2.metric("High Severity", sum(1 for f in findings if f.get("severity") == "HIGH"))
    col3.metric("Medium Severity", sum(1 for f in findings if f.get("severity") == "MEDIUM"))
    col4.metric("Low Severity", sum(1 for f in findings if f.get("severity") == "LOW"))

    st.markdown("---")
    st.subheader("Review Summary")
    st.info(f"{review.get('summary', 'No summary available')}\n\nReviewed file: `{data['fixture_path']}`")

    st.markdown("### Parsed Code Facts")
    if data["code_facts"]:
        for fact in data["code_facts"]:
            with st.expander(f"{fact.symbol_name} ({fact.start_line}-{fact.end_line})"):
                st.write(f"**File:** {fact.file_path}")
                st.write(f"**Language:** {fact.language}")
                st.code(fact.snippet, language="python")
    else:
        st.info("No code facts found.")

    st.markdown("### Findings")
    for idx, finding in enumerate(review["findings"], start=1):
        with st.expander(f"{idx}. {finding.get('severity', 'INFO')} — {finding.get('category', 'General')}"):
            st.write(f"**Message:** {finding.get('message', '')}")
            st.write(f"**Suggestion:** {finding.get('suggestion', '')}")
            st.write(f"**Agent:** {finding.get('agent_name', '')}")
            if finding.get("file_path"):
                st.write(f"**File:** {finding.get('file_path')}")
            if finding.get("line_start") or finding.get("line_end"):
                st.write(f"**Location:** {finding.get('line_start', 0)}-{finding.get('line_end', 0)}")

    st.markdown("---")
    st.markdown("### Formatted Review")
    st.code(data["formatted_review"], language="markdown")

else:
    st.info("Click **Run Review** to start the analysis.")