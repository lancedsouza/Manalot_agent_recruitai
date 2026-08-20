import tempfile
from pathlib import Path

import streamlit as st

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
Upload a resume, enter the candidate's role and business scope,
and evaluate the candidate against an appropriate professional benchmark.
"""
)


# ============================================================
# RESUME
# ============================================================

st.header("1. Resume")

uploaded_file = st.file_uploader(
    "Upload candidate resume",
    type=["pdf"],
)


# ============================================================
# UI CANDIDATE DETAILS
# ============================================================

st.header("2. Candidate Details")

col1, col2 = st.columns(2)

with col1:

    designation = st.text_input(
        "Designation",
        placeholder="Director"
    )

    function = st.text_input(
        "Function",
        placeholder="FP&A"
    )

    industry = st.text_input(
        "Industry",
        placeholder="Technology"
    )

    geography = st.text_input(
        "Geography",
        placeholder="India"
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
        placeholder="North America, MEA, UKI"
    )

    portfolio_handled = st.text_input(
        "Portfolio / Revenue Handled",
        placeholder="$400M"
    )


budget_handled = st.text_input(
    "Budget Handled",
    placeholder="$100M budget"
)


business_impact = st.text_area(
    "Business Impact",
    placeholder=(
        "Example: Reduced manual reporting by 90%, "
        "improved forecast accuracy by 15%..."
    )
)


transformation_scope = st.text_area(
    "Transformation / Strategic Scope",
    placeholder=(
        "Example: Led finance automation using Python, "
        "RPA and data platforms..."
    )
)


# ============================================================
# EVALUATE
# ============================================================

st.header("3. Evaluation")


if st.button(
    "Evaluate Candidate",
    type="primary",
    use_container_width=True,
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if uploaded_file is None:

        st.error(
            "Please upload a resume."
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
        # STEP 1 — TEMPORARILY SAVE PDF
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
        # STEP 2 — RESUME EXTRACTION
        # ====================================================

        with st.spinner(
            "Extracting resume experience, skills and education..."
        ):

            resume = extract_resume_data(
                temp_path
            )


        # ====================================================
        # STEP 3 — BUILD CANDIDATE PROFILE
        # ====================================================

        candidate_profile = CandidateProfile(

            # ----------------------------------------------
            # UI
            # ----------------------------------------------

            name=resume.name,

            designation=designation,

            function=function,

            industry=industry,

            experience_years=(
                resume.experience_years
            ),

            geography=geography,

            team_size=(
                team_size
                if team_size > 0
                else None
            ),

            largest_team_size=(
                largest_team_size
                if largest_team_size > 0
                else None
            ),

            markets=markets,

            portfolio_handled=(
                portfolio_handled
            ),

            budget_handled=(
                budget_handled
            ),

            business_impact=(
                business_impact
            ),

            transformation_scope=(
                transformation_scope
            ),

            # ----------------------------------------------
            # RESUME
            # ----------------------------------------------

            skills=resume.skills,

            experience_summary=str(
                resume.experience
            ),

            education_summary=str(
                resume.education
            ),
        )


        # ====================================================
        # STEP 4 — LANGGRAPH
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
        # STEP 5 — DISPLAY RESULTS
        # ====================================================

        st.success(
            "Candidate evaluation completed."
        )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

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
                f"{candidate_profile.experience_years:.1f} years",
            )


        with col3:

            st.metric(
                "Final Score",
                f"{result['final_score']:.2f} / 10",
            )


        # ----------------------------------------------------
        # RESUME DATA
        # ----------------------------------------------------

        with st.expander(
            "Resume Extraction"
        ):

            st.subheader(
                "Skills"
            )

            if resume.skills:

                st.write(
                    ", ".join(
                        resume.skills
                    )
                )

            else:

                st.write(
                    "No skills extracted."
                )


            st.subheader(
                "Experience"
            )

            for experience in resume.experience:

                st.write(
                    f"**{experience.title}** "
                    f"— {experience.company}"
                )

                st.write(
                    f"{experience.start_date} "
                    f"to {experience.end_date}"
                )


            st.subheader(
                "Education"
            )

            for education in resume.education:

                st.write(
                    f"**{education.degree}** "
                    f"— {education.institution}"
                )


        # ----------------------------------------------------
        # BENCHMARK
        # ----------------------------------------------------

        st.header(
            "Benchmark"
        )

        for dimension in (
            result["benchmark"].dimensions
        ):

            st.write(
                f"**{dimension.name}** "
                f"— Weight: "
                f"{dimension.weight:.0%}"
            )

            st.caption(
                dimension.description
            )


        # ----------------------------------------------------
        # DIMENSION SCORES
        # ----------------------------------------------------

        st.header(
            "Dimension Scores"
        )

        for item in (
            result["evaluation"]
            .dimension_scores
        ):

            st.subheader(
                f"{item.dimension}: "
                f"{item.score:.1f}/10"
            )

            st.write(
                item.analysis
            )


            if item.evidence:

                st.write(
                    "**Evidence:**"
                )

                for evidence in item.evidence:

                    st.write(
                        f"- {evidence}"
                    )


        # ----------------------------------------------------
        # STRENGTHS / WEAKNESSES
        # ----------------------------------------------------

        left, right = st.columns(2)


        with left:

            st.header(
                "Strengths"
            )

            for item in (
                result["evaluation"].strengths
            ):

                st.write(
                    f"- {item}"
                )


        with right:

            st.header(
                "Weaknesses"
            )

            for item in (
                result["evaluation"].weaknesses
            ):

                st.write(
                    f"- {item}"
                )


        # ----------------------------------------------------
        # IMPROVEMENTS
        # ----------------------------------------------------

        st.header(
            "Recommended Improvements"
        )

        for item in (
            result["evaluation"].improvements
        ):

            st.write(
                f"- {item}"
            )


        # ----------------------------------------------------
        # OVERALL ANALYSIS
        # ----------------------------------------------------

        st.header(
            "Overall Analysis"
        )

        st.write(
            result["evaluation"]
            .overall_analysis
        )


        # ----------------------------------------------------
        # DEBUG
        # ----------------------------------------------------

        with st.expander(
            "View Raw Result"
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