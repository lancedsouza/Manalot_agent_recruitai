import sys
import tempfile
from pathlib import Path

import streamlit as st


# ============================================================
# FIX IMPORT PATH FOR STREAMLIT CLOUD
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


# ============================================================
# PROJECT IMPORTS
# ============================================================

from app.services.resume_extractor import extract_resume_data
from app.models.candidate_profile import CandidateProfile
from app.agents.benchmark_graph import benchmark_graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Manalot RecruitAI",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("Manalot RecruitAI")

st.write(
    """
Upload a candidate resume, provide the candidate's professional
scope, and evaluate the candidate against an appropriate benchmark.
"""
)


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header("1. Resume")

uploaded_file = st.file_uploader(
    "Upload Candidate Resume",
    type=["pdf"],
)


# ============================================================
# UI DETAILS
# ============================================================

st.header("2. Candidate Details")

col1, col2 = st.columns(2)


with col1:

    designation = st.text_input(
        "Designation",
        placeholder="Director",
    )

    function = st.text_input(
        "Function",
        placeholder="FP&A",
    )

    industry = st.text_input(
        "Industry",
        placeholder="Technology",
    )

    geography = st.text_input(
        "Geography",
        placeholder="India",
    )


with col2:

    team_size = st.number_input(
        "Current Team Size",
        min_value=0,
        step=1,
        value=0,
    )

    largest_team_size = st.number_input(
        "Largest Team Size Managed",
        min_value=0,
        step=1,
        value=0,
    )

    markets = st.text_input(
        "Markets Handled",
        placeholder="North America, MEA, UKI",
    )

    portfolio_handled = st.text_input(
        "Portfolio / Revenue Handled",
        placeholder="$400M",
    )


budget_handled = st.text_input(
    "Budget Handled",
    placeholder="$100M budget",
)


business_impact = st.text_area(
    "Business Impact",
    placeholder=(
        "Example: Reduced manual reporting by 90%, "
        "improved forecast accuracy by 15%, "
        "reduced costs by $5M..."
    ),
)


transformation_scope = st.text_area(
    "Transformation / Strategic Scope",
    placeholder=(
        "Example: Led finance automation using Python, "
        "RPA, Power BI and data platforms..."
    ),
)


# ============================================================
# EVALUATION BUTTON
# ============================================================

st.header("3. Candidate Evaluation")

evaluate_button = st.button(
    "Evaluate Candidate",
    type="primary",
    use_container_width=True,
)


# ============================================================
# PROCESS
# ============================================================

if evaluate_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if uploaded_file is None:
        st.error(
            "Please upload the candidate resume."
        )
        st.stop()

    if not designation.strip():
        st.error(
            "Please enter the candidate designation."
        )
        st.stop()

    if not function.strip():
        st.error(
            "Please enter the candidate function."
        )
        st.stop()

    if not industry.strip():
        st.error(
            "Please enter the candidate industry."
        )
        st.stop()

    if not geography.strip():
        st.error(
            "Please enter the candidate geography."
        )
        st.stop()


    temp_path = None


    try:

        # ====================================================
        # STEP 1 — SAVE PDF TEMPORARILY
        # ====================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = Path(
                temp_file.name
            )


        # ====================================================
        # STEP 2 — EXTRACT RESUME
        # ====================================================

        with st.spinner(
            "Extracting experience, skills and education..."
        ):

            resume = extract_resume_data(
                temp_path
            )


        # ====================================================
        # STEP 3 — BUILD SUMMARIES
        # ====================================================

        experience_lines = []

        for experience in resume.experience:

            line = (
                f"{experience.title} at "
                f"{experience.company} "
                f"({experience.start_date} - "
                f"{experience.end_date})"
            )

            experience_lines.append(
                line
            )

        experience_summary = "\n".join(
            experience_lines
        )


        education_lines = []

        for education in resume.education:

            line = (
                f"{education.degree} at "
                f"{education.institution}"
            )

            if education.start_date or education.end_date:

                line += (
                    f" ({education.start_date} - "
                    f"{education.end_date})"
                )

            education_lines.append(
                line
            )

        education_summary = "\n".join(
            education_lines
        )


        # ====================================================
        # STEP 4 — BUILD CANDIDATE PROFILE
        # ====================================================

        candidate_profile = CandidateProfile(

            # ------------------------------------------------
            # RESUME
            # ------------------------------------------------

            name=resume.name,

            experience_years=(
                resume.experience_years
            ),

            skills=resume.skills,

            experience_summary=(
                experience_summary
            ),

            education_summary=(
                education_summary
            ),

            # ------------------------------------------------
            # UI
            # ------------------------------------------------

            designation=designation.strip(),

            function=function.strip(),

            industry=industry.strip(),

            geography=geography.strip(),

            team_size=(
                int(team_size)
                if team_size > 0
                else None
            ),

            largest_team_size=(
                int(largest_team_size)
                if largest_team_size > 0
                else None
            ),

            markets=markets.strip(),

            portfolio_handled=(
                portfolio_handled.strip()
            ),

            budget_handled=(
                budget_handled.strip()
            ),

            business_impact=(
                business_impact.strip()
            ),

            transformation_scope=(
                transformation_scope.strip()
            ),
        )


        # ====================================================
        # STEP 5 — RUN LANGGRAPH
        # ====================================================

        with st.spinner(
            "Benchmarking candidate..."
        ):

            result = benchmark_graph.invoke(
                {
                    "candidate_profile":
                    candidate_profile
                }
            )


        # ====================================================
        # SUCCESS
        # ====================================================

        st.success(
            "Candidate evaluation completed."
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        st.divider()

        st.header(
            "Candidate Summary"
        )

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Candidate",
                candidate_profile.name,
            )


        with col2:

            st.metric(
                "Experience",
                (
                    f"{candidate_profile.experience_years:.1f} "
                    f"years"
                ),
            )


        with col3:

            st.metric(
                "Final Score",
                f"{result['final_score']:.2f} / 10",
            )


        # ====================================================
        # RESUME EXTRACTION
        # ====================================================

        with st.expander(
            "Resume Extraction",
            expanded=False,
        ):

            st.subheader(
                "Skills"
            )

            if resume.skills:

                for skill in resume.skills:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.info(
                    "No skills extracted."
                )


            st.subheader(
                "Professional Experience"
            )

            if resume.experience:

                for experience in resume.experience:

                    st.markdown(
                        f"**{experience.title}**"
                    )

                    st.write(
                        f"Company: {experience.company}"
                    )

                    st.write(
                        f"Period: "
                        f"{experience.start_date} "
                        f"to "
                        f"{experience.end_date}"
                    )

                    st.write("---")

            else:

                st.info(
                    "No experience extracted."
                )


            st.subheader(
                "Education"
            )

            if resume.education:

                for education in resume.education:

                    st.markdown(
                        f"**{education.degree}**"
                    )

                    st.write(
                        f"Institution: "
                        f"{education.institution}"
                    )

                    if (
                        education.start_date
                        or education.end_date
                    ):

                        st.write(
                            f"Period: "
                            f"{education.start_date} "
                            f"to "
                            f"{education.end_date}"
                        )

                    st.write("---")

            else:

                st.info(
                    "No education extracted."
                )


        # ====================================================
        # BENCHMARK
        # ====================================================

        st.divider()

        st.header(
            "Benchmark Used"
        )

        st.write(
            f"**Function:** "
            f"{result['benchmark'].function}"
        )


        for dimension in (
            result["benchmark"].dimensions
        ):

            st.markdown(
                f"### {dimension.name}"
            )

            st.write(
                f"Weight: "
                f"{dimension.weight:.0%}"
            )

            st.caption(
                dimension.description
            )


        # ====================================================
        # DIMENSION SCORES
        # ====================================================

        st.divider()

        st.header(
            "Dimension Scores"
        )


        for item in (
            result["evaluation"]
            .dimension_scores
        ):

            st.subheader(
                f"{item.dimension} — "
                f"{item.score:.1f}/10"
            )

            st.progress(
                min(
                    max(
                        item.score / 10,
                        0.0,
                    ),
                    1.0,
                )
            )

            st.write(
                item.analysis
            )


            if item.evidence:

                st.markdown(
                    "**Evidence**"
                )

                for evidence in item.evidence:

                    st.write(
                        f"• {evidence}"
                    )


        # ====================================================
        # STRENGTHS + WEAKNESSES
        # ====================================================

        st.divider()

        left, right = st.columns(2)


        with left:

            st.header(
                "Strengths"
            )

            if result["evaluation"].strengths:

                for strength in (
                    result["evaluation"]
                    .strengths
                ):

                    st.write(
                        f"• {strength}"
                    )

            else:

                st.info(
                    "No specific strengths identified."
                )


        with right:

            st.header(
                "Weaknesses / Gaps"
            )

            if result["evaluation"].weaknesses:

                for weakness in (
                    result["evaluation"]
                    .weaknesses
                ):

                    st.write(
                        f"• {weakness}"
                    )

            else:

                st.info(
                    "No major weaknesses identified."
                )


        # ====================================================
        # IMPROVEMENTS
        # ====================================================

        st.divider()

        st.header(
            "Recommended Improvements"
        )


        if result["evaluation"].improvements:

            for improvement in (
                result["evaluation"]
                .improvements
            ):

                st.write(
                    f"• {improvement}"
                )

        else:

            st.info(
                "No specific improvements returned."
            )


        # ====================================================
        # OVERALL ANALYSIS
        # ====================================================

        st.divider()

        st.header(
            "Overall Analysis"
        )

        st.write(
            result["evaluation"]
            .overall_analysis
        )


        # ====================================================
        # RAW DATA
        # ====================================================

        with st.expander(
            "Developer View — Raw Result",
            expanded=False,
        ):

            st.json(
                {
                    "candidate_profile":
                    candidate_profile.model_dump(),

                    "benchmark":
                    result[
                        "benchmark"
                    ].model_dump(),

                    "evaluation":
                    result[
                        "evaluation"
                    ].model_dump(),

                    "final_score":
                    result[
                        "final_score"
                    ],
                }
            )


    except Exception as e:

        st.error(
            "Candidate evaluation failed."
        )

        st.exception(
            e
        )


    finally:

        if (
            temp_path is not None
            and temp_path.exists()
        ):

            temp_path.unlink()