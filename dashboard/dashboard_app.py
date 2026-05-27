from pathlib import Path
import sys
from dataclasses import asdict
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.parser.tree_parser import parse_file
from app.agents.security import run_security_agent
from app.agents.logic import run_logic_agent
from app.agents.style import run_style_agent
from app.reviewer.aggregator import aggregate_findings
from app.reviewer.formatter import format_review_markdown
from app.utils.text_cleaner import clean_text


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Code Review Dashboard",
    layout="wide"
)

st.title("AI Code Review Dashboard")

st.markdown(
    "Upload Python, C++, Java or JavaScript code and let AI review it."
)

if "review_data" not in st.session_state:
    st.session_state.review_data = None


# ==========================
# LANGUAGE DETECTOR
# ==========================

def detect_language(filename):

    ext = Path(filename).suffix.lower()

    mapping = {
        ".py":"python",
        ".cpp":"cpp",
        ".c":"c",
        ".java":"java",
        ".js":"javascript"
    }

    return mapping.get(
        ext,
        "unknown"
    )


# ==========================
# FILE UPLOAD
# ==========================

uploaded_file = st.file_uploader(
    "Upload code file",
    type=[
        "py",
        "cpp",
        "c",
        "java",
        "js"
    ]
)


# ==========================
# RUN REVIEW
# ==========================

if st.button("Run Review"):

    if uploaded_file is None:

        st.warning(
            "Please upload a file"
        )

        st.stop()


    with st.spinner(
        "Running AI Review..."
    ):

        try:

            content = uploaded_file.read().decode(
                "utf-8"
            )

            file_name = uploaded_file.name

            language = detect_language(
                file_name
            )


            # Parse only Python for now

            if language=="python":

                try:

                    code_facts = parse_file(
                        file_name,
                        content,
                        []
                    )

                except:

                    code_facts=[]

            else:

                code_facts=[]


            # Agent calls

            security_findings = run_security_agent(
                content
            )

            logic_findings = run_logic_agent(
                content
            )

            style_findings = run_style_agent(
                content
            )


            findings=[]

            for f in (

                security_findings+
                logic_findings+
                style_findings

            ):

                try:

                    findings.append(
                        asdict(f)
                    )

                except:

                    findings.append(
                        f
                    )


            review = aggregate_findings(
                findings
            )

            formatted_review = format_review_markdown(
                review
            )


            st.session_state.review_data={

                "file_name":file_name,
                "language":language,
                "content":content,
                "code_facts":code_facts,
                "findings":findings,
                "review":review,
                "formatted_review":formatted_review

            }


            st.success(
                "Review Complete"
            )

        except Exception:

            st.error(
                "Review failed. Please try again."
            )


# ==========================
# RESULTS
# ==========================

if st.session_state.review_data:

    data=st.session_state.review_data

    findings=data["findings"]

    review=data["review"]

    st.markdown("---")

    st.subheader(
        "File Details"
    )

    c1,c2=st.columns(2)

    c1.info(
        f"File: {data['file_name']}"
    )

    c2.info(
        f"Language: {data['language']}"
    )


    st.subheader(
        "Code Preview"
    )

    st.code(
        data["content"]
    )


    st.markdown("---")


    a,b,c,d=st.columns(4)

    a.metric(
        "Total",
        len(findings)
    )

    b.metric(
        "High",
        sum(
            1
            for x in findings
            if x.get(
                "severity"
            )=="HIGH"
        )
    )

    c.metric(
        "Medium",
        sum(
            1
            for x in findings
            if x.get(
                "severity"
            )=="MEDIUM"
        )
    )

    d.metric(
        "Low",
        sum(
            1
            for x in findings
            if x.get(
                "severity"
            )=="LOW"
        )
    )


    st.markdown("---")

    st.subheader(
        "Review Summary"
    )

    st.info(
        review.summary
    )


    st.subheader(
        "Findings"
    )

    for i,finding in enumerate(
        findings,
        start=1
    ):

        with st.expander(

            f"{i}. "
            f"{finding.get('severity','INFO')} - "
            f"{finding.get('category','General')}"

        ):

            st.write(
                f"Message: {clean_text(finding.get('message',''))}"
            )

            st.write(
                f"Suggestion: {clean_text(finding.get('suggestion',''))}"
            )

            st.write(
                f"Agent: {finding.get('agent_name','')}"
            )


    st.subheader(
        "Formatted Review"
    )

    st.code(
        clean_text(data["formatted_review"]),
        language="markdown"
    )


else:

    st.info(
        "Upload a file and click Run Review"
    )