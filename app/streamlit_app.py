# import logging
# import sys
# import tempfile
# import time
# from pathlib import Path

# import streamlit as st


# # ============================================================
# # LOGGING
# # ============================================================

# logging.basicConfig(
#     level=logging.INFO,
#     format=(
#         "%(asctime)s | "
#         "%(levelname)s | "
#         "%(name)s | "
#         "%(message)s"
#     ),
# )

# logger = logging.getLogger(__name__)


# # ============================================================
# # FIX IMPORT PATH FOR STREAMLIT CLOUD
# # ============================================================

# PROJECT_ROOT = Path(__file__).resolve().parents[1]

# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(
#         0,
#         str(PROJECT_ROOT),
#     )


# # ============================================================
# # PROJECT IMPORTS
# # ============================================================

# from app.services.resume_extractor import extract_resume_data
# from app.models.candidate_profile import CandidateProfile
# from app.agents.benchmark_graph import benchmark_graph


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Manalot RecruitAI",
#     page_icon="📊",
#     layout="wide",
# )


# # ============================================================
# # HEADER
# # ============================================================

# st.title("Manalot RecruitAI")

# st.write(
#     """
# Upload a candidate resume, provide the candidate's professional
# scope, and evaluate the candidate against an appropriate benchmark.
# """
# )


# # ============================================================
# # RESUME UPLOAD
# # ============================================================

# st.header("1. Resume")

# uploaded_file = st.file_uploader(
#     "Upload Candidate Resume",
#     type=["pdf"],
# )


# # ============================================================
# # UI DETAILS
# # ============================================================

# st.header("2. Candidate Details")

# col1, col2 = st.columns(2)


# with col1:

#     designation = st.text_input(
#         "Designation",
#         placeholder="Director",
#     )

#     function = st.text_input(
#         "Function",
#         placeholder="FP&A",
#     )

#     industry = st.text_input(
#         "Industry",
#         placeholder="Technology",
#     )

#     geography = st.text_input(
#         "Geography",
#         placeholder="India",
#     )


# with col2:

#     team_size = st.number_input(
#         "Current Team Size",
#         min_value=0,
#         step=1,
#         value=0,
#     )

#     largest_team_size = st.number_input(
#         "Largest Team Size Managed",
#         min_value=0,
#         step=1,
#         value=0,
#     )

#     markets = st.text_input(
#         "Markets Handled",
#         placeholder="North America, MEA, UKI",
#     )

#     portfolio_handled = st.text_input(
#         "Portfolio / Revenue Handled",
#         placeholder="$400M",
#     )


# budget_handled = st.text_input(
#     "Budget Handled",
#     placeholder="$100M budget",
# )


# business_impact = st.text_area(
#     "Business Impact",
#     placeholder=(
#         "Example: Reduced manual reporting by 90%, "
#         "improved forecast accuracy by 15%, "
#         "reduced costs by $5M..."
#     ),
# )


# transformation_scope = st.text_area(
#     "Transformation / Strategic Scope",
#     placeholder=(
#         "Example: Led finance automation using Python, "
#         "RPA, Power BI and data platforms..."
#     ),
# )


# # ============================================================
# # EVALUATION BUTTON
# # ============================================================

# st.header("3. Candidate Evaluation")

# evaluate_button = st.button(
#     "Evaluate Candidate",
#     type="primary",
#     use_container_width=True,
# )


# # ============================================================
# # PROCESS
# # ============================================================

# if evaluate_button:

#     total_start = time.perf_counter()

#     logger.info("=" * 60)
#     logger.info("UI evaluation flow started")
#     logger.info("=" * 60)

#     # --------------------------------------------------------
#     # VALIDATION
#     # --------------------------------------------------------

#     if uploaded_file is None:
#         st.error(
#             "Please upload the candidate resume."
#         )
#         st.stop()

#     if not designation.strip():
#         st.error(
#             "Please enter the candidate designation."
#         )
#         st.stop()

#     if not function.strip():
#         st.error(
#             "Please enter the candidate function."
#         )
#         st.stop()

#     if not industry.strip():
#         st.error(
#             "Please enter the candidate industry."
#         )
#         st.stop()

#     if not geography.strip():
#         st.error(
#             "Please enter the candidate geography."
#         )
#         st.stop()


#     temp_path = None

#     # --------------------------------------------------------
#     # Visible UI status container
#     # --------------------------------------------------------

#     status_box = st.status(
#         "Starting candidate evaluation...",
#         expanded=True,
#     )


#     try:

#         # ====================================================
#         # STEP 1 — SAVE PDF
#         # ====================================================

#         step_start = time.perf_counter()

#         status_box.write(
#             "1. Saving uploaded PDF..."
#         )

#         logger.info(
#             "STEP 1: Saving uploaded PDF."
#         )

#         with tempfile.NamedTemporaryFile(
#             delete=False,
#             suffix=".pdf",
#         ) as temp_file:

#             temp_file.write(
#                 uploaded_file.getbuffer()
#             )

#             temp_path = Path(
#                 temp_file.name
#             )

#         elapsed = (
#             time.perf_counter()
#             - step_start
#         )

#         logger.info(
#             "STEP 1 complete in %.4f seconds.",
#             elapsed,
#         )

#         status_box.write(
#             f"✓ PDF saved in {elapsed:.2f}s"
#         )


#         # ====================================================
#         # STEP 2 — RESUME EXTRACTION
#         # ====================================================

#         step_start = time.perf_counter()

#         status_box.write(
#             "2. Extracting resume information..."
#         )

#         logger.info(
#             "STEP 2: Starting resume extraction."
#         )

#         try:

#             resume = extract_resume_data(
#                 temp_path
#             )

#         except Exception:

#             elapsed = (
#                 time.perf_counter()
#                 - step_start
#             )

#             logger.exception(
#                 "STEP 2 FAILED after %.2f seconds.",
#                 elapsed,
#             )

#             status_box.update(
#                 label=(
#                     "Resume extraction failed"
#                 ),
#                 state="error",
#             )

#             raise


#         elapsed = (
#             time.perf_counter()
#             - step_start
#         )

#         logger.info(
#             "STEP 2 complete in %.2f seconds.",
#             elapsed,
#         )

#         status_box.write(
#             f"✓ Resume extraction completed "
#             f"in {elapsed:.2f}s"
#         )


#         # ====================================================
#         # STEP 3 — BUILD SUMMARIES
#         # ====================================================

#         step_start = time.perf_counter()

#         status_box.write(
#             "3. Building candidate summaries..."
#         )

#         logger.info(
#             "STEP 3: Building experience "
#             "and education summaries."
#         )

#         experience_lines = []

#         for experience in resume.experience:

#             line = (
#                 f"{experience.title} at "
#                 f"{experience.company} "
#                 f"({experience.start_date} - "
#                 f"{experience.end_date})"
#             )

#             experience_lines.append(
#                 line
#             )


#         experience_summary = "\n".join(
#             experience_lines
#         )


#         education_lines = []

#         for education in resume.education:

#             line = (
#                 f"{education.degree} at "
#                 f"{education.institution}"
#             )

#             if (
#                 education.start_date
#                 or education.end_date
#             ):

#                 line += (
#                     f" ({education.start_date} - "
#                     f"{education.end_date})"
#                 )

#             education_lines.append(
#                 line
#             )


#         education_summary = "\n".join(
#             education_lines
#         )


#         elapsed = (
#             time.perf_counter()
#             - step_start
#         )

#         logger.info(
#             "STEP 3 complete in %.4f seconds.",
#             elapsed,
#         )

#         status_box.write(
#             f"✓ Candidate summaries built "
#             f"in {elapsed:.2f}s"
#         )


#         # ====================================================
#         # STEP 4 — BUILD CANDIDATE PROFILE
#         # ====================================================

#         step_start = time.perf_counter()

#         status_box.write(
#             "4. Building candidate profile..."
#         )

#         logger.info(
#             "STEP 4: Building CandidateProfile."
#         )

#         candidate_profile = CandidateProfile(

#             name=resume.name,

#             experience_years=(
#                 resume.experience_years
#             ),

#             skills=resume.skills,

#             experience_summary=(
#                 experience_summary
#             ),

#             education_summary=(
#                 education_summary
#             ),

#             designation=designation.strip(),

#             function=function.strip(),

#             industry=industry.strip(),

#             geography=geography.strip(),

#             team_size=(
#                 int(team_size)
#                 if team_size > 0
#                 else None
#             ),

#             largest_team_size=(
#                 int(largest_team_size)
#                 if largest_team_size > 0
#                 else None
#             ),

#             markets=markets.strip(),

#             portfolio_handled=(
#                 portfolio_handled.strip()
#             ),

#             budget_handled=(
#                 budget_handled.strip()
#             ),

#             business_impact=(
#                 business_impact.strip()
#             ),

#             transformation_scope=(
#                 transformation_scope.strip()
#             ),
#         )


#         elapsed = (
#             time.perf_counter()
#             - step_start
#         )

#         logger.info(
#             "STEP 4 complete in %.4f seconds.",
#             elapsed,
#         )

#         logger.info(
#             "Candidate profile size: %d characters.",
#             len(
#                 candidate_profile.model_dump_json()
#             ),
#         )

#         status_box.write(
#             f"✓ Candidate profile built "
#             f"in {elapsed:.2f}s"
#         )


#         # ====================================================
#         # STEP 5 — BENCHMARK + EVALUATION
#         # ====================================================

#         step_start = time.perf_counter()

#         status_box.write(
#             "5. Generating benchmark and "
#             "evaluating candidate..."
#         )

#         logger.info(
#             "STEP 5: Starting LangGraph."
#         )

#         try:

#             result = benchmark_graph.invoke(
#                 {
#                     "candidate_profile":
#                     candidate_profile
#                 }
#             )

#         except Exception:

#             elapsed = (
#                 time.perf_counter()
#                 - step_start
#             )

#             logger.exception(
#                 "STEP 5 FAILED after %.2f seconds.",
#                 elapsed,
#             )

#             status_box.update(
#                 label=(
#                     "Benchmark or candidate "
#                     "evaluation failed"
#                 ),
#                 state="error",
#             )

#             raise


#         elapsed = (
#             time.perf_counter()
#             - step_start
#         )

#         logger.info(
#             "STEP 5 complete in %.2f seconds.",
#             elapsed,
#         )

#         status_box.write(
#             f"✓ Benchmark/evaluation completed "
#             f"in {elapsed:.2f}s"
#         )


#         # ====================================================
#         # COMPLETE
#         # ====================================================

#         total_elapsed = (
#             time.perf_counter()
#             - total_start
#         )

#         logger.info("=" * 60)

#         logger.info(
#             "TOTAL UI FLOW completed in %.2f seconds.",
#             total_elapsed,
#         )

#         logger.info("=" * 60)


#         status_box.update(
#             label=(
#                 f"Candidate evaluation completed "
#                 f"in {total_elapsed:.1f}s"
#             ),
#             state="complete",
#             expanded=False,
#         )


#         # ====================================================
#         # SUCCESS
#         # ====================================================

#         st.success(
#             "Candidate evaluation completed."
#         )


#         # ====================================================
#         # SUMMARY
#         # ====================================================

#         st.divider()

#         st.header(
#             "Candidate Summary"
#         )

#         col1, col2, col3 = st.columns(3)


#         with col1:

#             st.metric(
#                 "Candidate",
#                 candidate_profile.name,
#             )


#         with col2:

#             st.metric(
#                 "Experience",
#                 (
#                     f"{candidate_profile.experience_years:.1f} "
#                     f"years"
#                 ),
#             )


#         with col3:

#             st.metric(
#                 "Final Score",
#                 f"{result['final_score']:.2f} / 10",
#             )


#         # ====================================================
#         # RESUME EXTRACTION
#         # ====================================================

#         with st.expander(
#             "Resume Extraction",
#             expanded=False,
#         ):

#             st.subheader(
#                 "Skills"
#             )

#             if resume.skills:

#                 for skill in resume.skills:

#                     st.write(
#                         f"• {skill}"
#                     )

#             else:

#                 st.info(
#                     "No skills extracted."
#                 )


#             st.subheader(
#                 "Professional Experience"
#             )

#             if resume.experience:

#                 for experience in resume.experience:

#                     st.markdown(
#                         f"**{experience.title}**"
#                     )

#                     st.write(
#                         f"Company: {experience.company}"
#                     )

#                     st.write(
#                         f"Period: "
#                         f"{experience.start_date} "
#                         f"to "
#                         f"{experience.end_date}"
#                     )

#                     st.write("---")

#             else:

#                 st.info(
#                     "No experience extracted."
#                 )


#             st.subheader(
#                 "Education"
#             )

#             if resume.education:

#                 for education in resume.education:

#                     st.markdown(
#                         f"**{education.degree}**"
#                     )

#                     st.write(
#                         f"Institution: "
#                         f"{education.institution}"
#                     )

#                     if (
#                         education.start_date
#                         or education.end_date
#                     ):

#                         st.write(
#                             f"Period: "
#                             f"{education.start_date} "
#                             f"to "
#                             f"{education.end_date}"
#                         )

#                     st.write("---")

#             else:

#                 st.info(
#                     "No education extracted."
#                 )


#         # ====================================================
#         # BENCHMARK
#         # ====================================================

#         st.divider()

#         st.header(
#             "Benchmark Used"
#         )

#         st.write(
#             f"**Function:** "
#             f"{result['benchmark'].function}"
#         )


#         for dimension in (
#             result["benchmark"].dimensions
#         ):

#             st.markdown(
#                 f"### {dimension.name}"
#             )

#             st.write(
#                 f"Weight: "
#                 f"{dimension.weight:.0%}"
#             )

#             st.caption(
#                 dimension.description
#             )


#         # ====================================================
#         # DIMENSION SCORES
#         # ====================================================

#         st.divider()

#         st.header(
#             "Dimension Scores"
#         )


#         for item in (
#             result["evaluation"]
#             .dimension_scores
#         ):

#             st.subheader(
#                 f"{item.dimension} — "
#                 f"{item.score:.1f}/10"
#             )

#             st.progress(
#                 min(
#                     max(
#                         item.score / 10,
#                         0.0,
#                     ),
#                     1.0,
#                 )
#             )

#             st.write(
#                 item.analysis
#             )


#             if item.evidence:

#                 st.markdown(
#                     "**Evidence**"
#                 )

#                 for evidence in item.evidence:

#                     st.write(
#                         f"• {evidence}"
#                     )


#         # ====================================================
#         # STRENGTHS + WEAKNESSES
#         # ====================================================

#         st.divider()

#         left, right = st.columns(2)


#         with left:

#             st.header(
#                 "Strengths"
#             )

#             if result["evaluation"].strengths:

#                 for strength in (
#                     result["evaluation"]
#                     .strengths
#                 ):

#                     st.write(
#                         f"• {strength}"
#                     )

#             else:

#                 st.info(
#                     "No specific strengths identified."
#                 )


#         with right:

#             st.header(
#                 "Weaknesses / Gaps"
#             )

#             if result["evaluation"].weaknesses:

#                 for weakness in (
#                     result["evaluation"]
#                     .weaknesses
#                 ):

#                     st.write(
#                         f"• {weakness}"
#                     )

#             else:

#                 st.info(
#                     "No major weaknesses identified."
#                 )


#         # ====================================================
#         # IMPROVEMENTS
#         # ====================================================

#         st.divider()

#         st.header(
#             "Recommended Improvements"
#         )


#         if result["evaluation"].improvements:

#             for improvement in (
#                 result["evaluation"]
#                 .improvements
#             ):

#                 st.write(
#                     f"• {improvement}"
#                 )

#         else:

#             st.info(
#                 "No specific improvements returned."
#             )


#         # ====================================================
#         # OVERALL ANALYSIS
#         # ====================================================

#         st.divider()

#         st.header(
#             "Overall Analysis"
#         )

#         st.write(
#             result["evaluation"]
#             .overall_analysis
#         )


#         # ====================================================
#         # RAW DATA
#         # ====================================================

#         with st.expander(
#             "Developer View — Raw Result",
#             expanded=False,
#         ):

#             st.json(
#                 {
#                     "candidate_profile":
#                     candidate_profile.model_dump(),

#                     "benchmark":
#                     result[
#                         "benchmark"
#                     ].model_dump(),

#                     "evaluation":
#                     result[
#                         "evaluation"
#                     ].model_dump(),

#                     "final_score":
#                     result[
#                         "final_score"
#                     ],
#                 }
#             )


#     # ========================================================
#     # ERROR HANDLING
#     # ========================================================

#     except Exception as e:

#         total_elapsed = (
#             time.perf_counter()
#             - total_start
#         )

#         logger.exception(
#             "UI candidate evaluation FAILED "
#             "after %.2f seconds.",
#             total_elapsed,
#         )

#         st.error(
#             "Candidate evaluation failed."
#         )

#         st.exception(
#             e
#         )


#     # ========================================================
#     # CLEANUP
#     # ========================================================

#     finally:

#         if (
#             temp_path is not None
#             and temp_path.exists()
#         ):

#             try:

#                 temp_path.unlink()

#                 logger.info(
#                     "Temporary PDF deleted."
#                 )

#             except Exception:

#                 logger.exception(
#                     "Could not delete temporary PDF."
#                 )

import logging
import sys
import tempfile
import time
from pathlib import Path

import streamlit as st
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


# ============================================================
# FIX IMPORT PATH FOR STREAMLIT CLOUD / LOCAL EXECUTION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

# Existing Candidate Benchmark imports
from app.services.resume_extractor import extract_resume_data
from app.models.candidate_profile import CandidateProfile
from app.agents.benchmark_graph import benchmark_graph

# New JD Matcher imports
from app.db_jd.db import SessionLocal
from app.db_jd.jd_models import JD
from app.services.embedding_service import create_embedding
from app.utils.similarity import similarity
import streamlit as st

from app.db_jd.init_db_jd import init_db


@st.cache_resource
def initialize_database():
    init_db()


initialize_database()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Manalot RecruitAI",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# SHARED DOCUMENT TEXT EXTRACTION
# ============================================================

def extract_uploaded_document(uploaded_file) -> str:
    """Extract full text from a Streamlit PDF or DOCX upload."""

    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix not in {".pdf", ".docx"}:
        raise ValueError(f"Unsupported file type: {suffix}")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = Path(temp_file.name)

        if suffix == ".pdf":
            loader = PyPDFLoader(str(temp_path))
        else:
            loader = Docx2txtLoader(str(temp_path))

        docs = loader.load()

        full_text = "\n".join(
            doc.page_content
            for doc in docs
            if doc.page_content
        )

        return full_text.strip()

    finally:
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                logger.exception("Could not delete temporary document.")


# ============================================================
# SAVE ONE COMPLETE JD
# ============================================================

def create_and_save_jd(designation: str, jd_text: str):
    """Embed the complete JD once and save one JD row."""

    if not designation.strip():
        raise ValueError("Designation cannot be empty.")

    if not jd_text.strip():
        raise ValueError("JD text cannot be empty.")

    # Same embedding model used for both JD and resumes.
    jd_embedding = create_embedding(jd_text)

    jd_record = JD(
        title=designation.strip(),
        description=jd_text,
        embedding=jd_embedding,
    )

    session = SessionLocal()

    try:
        session.add(jd_record)
        session.commit()
        session.refresh(jd_record)

        return {
            "id": jd_record.chunk_index,
            "title": jd_record.title,
            "embedding": jd_embedding,
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


# ============================================================
# MATCH MULTIPLE UPLOADED RESUMES AGAINST ONE JD
# ============================================================

def match_uploaded_resumes(jd_embedding, resumes):
    """Embed each full resume and rank it against the full JD embedding."""

    results = []

    for resume in resumes:
        resume_text = resume["text"]

        if not resume_text.strip():
            continue

        resume_embedding = create_embedding(resume_text)

        score = similarity(
            jd_embedding,
            resume_embedding,
        )

        results.append(
            {
                "Candidate": resume["name"],
                "Match Score": round(float(score), 4),
            }
        )

    results.sort(
        key=lambda item: item["Match Score"],
        reverse=True,
    )

    return results


# ============================================================
# EXISTING CANDIDATE BENCHMARK PAGE
# ============================================================

def show_candidate_benchmark():
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

        total_start = time.perf_counter()

        logger.info("=" * 60)
        logger.info("UI evaluation flow started")
        logger.info("=" * 60)

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

        # --------------------------------------------------------
        # Visible UI status container
        # --------------------------------------------------------

        status_box = st.status(
            "Starting candidate evaluation...",
            expanded=True,
        )


        try:

            # ====================================================
            # STEP 1 — SAVE PDF
            # ====================================================

            step_start = time.perf_counter()

            status_box.write(
                "1. Saving uploaded PDF..."
            )

            logger.info(
                "STEP 1: Saving uploaded PDF."
            )

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

            elapsed = (
                time.perf_counter()
                - step_start
            )

            logger.info(
                "STEP 1 complete in %.4f seconds.",
                elapsed,
            )

            status_box.write(
                f"✓ PDF saved in {elapsed:.2f}s"
            )


            # ====================================================
            # STEP 2 — RESUME EXTRACTION
            # ====================================================

            step_start = time.perf_counter()

            status_box.write(
                "2. Extracting resume information..."
            )

            logger.info(
                "STEP 2: Starting resume extraction."
            )

            try:

                resume = extract_resume_data(
                    temp_path
                )

            except Exception:

                elapsed = (
                    time.perf_counter()
                    - step_start
                )

                logger.exception(
                    "STEP 2 FAILED after %.2f seconds.",
                    elapsed,
                )

                status_box.update(
                    label=(
                        "Resume extraction failed"
                    ),
                    state="error",
                )

                raise


            elapsed = (
                time.perf_counter()
                - step_start
            )

            logger.info(
                "STEP 2 complete in %.2f seconds.",
                elapsed,
            )

            status_box.write(
                f"✓ Resume extraction completed "
                f"in {elapsed:.2f}s"
            )


            # ====================================================
            # STEP 3 — BUILD SUMMARIES
            # ====================================================

            step_start = time.perf_counter()

            status_box.write(
                "3. Building candidate summaries..."
            )

            logger.info(
                "STEP 3: Building experience "
                "and education summaries."
            )

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

                if (
                    education.start_date
                    or education.end_date
                ):

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


            elapsed = (
                time.perf_counter()
                - step_start
            )

            logger.info(
                "STEP 3 complete in %.4f seconds.",
                elapsed,
            )

            status_box.write(
                f"✓ Candidate summaries built "
                f"in {elapsed:.2f}s"
            )


            # ====================================================
            # STEP 4 — BUILD CANDIDATE PROFILE
            # ====================================================

            step_start = time.perf_counter()

            status_box.write(
                "4. Building candidate profile..."
            )

            logger.info(
                "STEP 4: Building CandidateProfile."
            )

            candidate_profile = CandidateProfile(

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


            elapsed = (
                time.perf_counter()
                - step_start
            )

            logger.info(
                "STEP 4 complete in %.4f seconds.",
                elapsed,
            )

            logger.info(
                "Candidate profile size: %d characters.",
                len(
                    candidate_profile.model_dump_json()
                ),
            )

            status_box.write(
                f"✓ Candidate profile built "
                f"in {elapsed:.2f}s"
            )


            # ====================================================
            # STEP 5 — BENCHMARK + EVALUATION
            # ====================================================

            step_start = time.perf_counter()

            status_box.write(
                "5. Generating benchmark and "
                "evaluating candidate..."
            )

            logger.info(
                "STEP 5: Starting LangGraph."
            )

            try:

                result = benchmark_graph.invoke(
                    {
                        "candidate_profile":
                        candidate_profile
                    }
                )

            except Exception:

                elapsed = (
                    time.perf_counter()
                    - step_start
                )

                logger.exception(
                    "STEP 5 FAILED after %.2f seconds.",
                    elapsed,
                )

                status_box.update(
                    label=(
                        "Benchmark or candidate "
                        "evaluation failed"
                    ),
                    state="error",
                )

                raise


            elapsed = (
                time.perf_counter()
                - step_start
            )

            logger.info(
                "STEP 5 complete in %.2f seconds.",
                elapsed,
            )

            status_box.write(
                f"✓ Benchmark/evaluation completed "
                f"in {elapsed:.2f}s"
            )


            # ====================================================
            # COMPLETE
            # ====================================================

            total_elapsed = (
                time.perf_counter()
                - total_start
            )

            logger.info("=" * 60)

            logger.info(
                "TOTAL UI FLOW completed in %.2f seconds.",
                total_elapsed,
            )

            logger.info("=" * 60)


            status_box.update(
                label=(
                    f"Candidate evaluation completed "
                    f"in {total_elapsed:.1f}s"
                ),
                state="complete",
                expanded=False,
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


        # ========================================================
        # ERROR HANDLING
        # ========================================================

        except Exception as e:

            total_elapsed = (
                time.perf_counter()
                - total_start
            )

            logger.exception(
                "UI candidate evaluation FAILED "
                "after %.2f seconds.",
                total_elapsed,
            )

            st.error(
                "Candidate evaluation failed."
            )

            st.exception(
                e
            )


        # ========================================================
        # CLEANUP
        # ========================================================

        finally:

            if (
                temp_path is not None
                and temp_path.exists()
            ):

                try:

                    temp_path.unlink()

                    logger.info(
                        "Temporary PDF deleted."
                    )

                except Exception:

                    logger.exception(
                        "Could not delete temporary PDF."
                    )

# ============================================================
# JD CANDIDATE MATCHER PAGE
# ============================================================

def show_jd_candidate_matcher():

    st.title("🎯 JD Candidate Matcher")

    st.write(
        "Upload one job description and multiple candidate resumes. "
        "The MVP compares the complete JD embedding with each complete "
        "resume embedding and ranks candidates by cosine similarity."
    )

    st.info(
        "For this MVP, skills, experience, responsibilities and other "
        "resume content influence the semantic similarity because they are "
        "part of the full resume text. They are not yet scored as separate "
        "structured components."
    )

    st.divider()

    # --------------------------------------------------------
    # STEP 1 — JOB DETAILS
    # --------------------------------------------------------

    st.header("1. Job Details")

    designation = st.text_input(
        "Job Designation",
        placeholder="e.g. Senior Manager - FP&A",
        key="matcher_designation",
    )

    jd_file = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx"],
        key="matcher_jd_upload",
    )

    st.divider()

    # --------------------------------------------------------
    # STEP 2 — CANDIDATE RESUMES
    # --------------------------------------------------------

    st.header("2. Candidate Resumes")

    resume_files = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="matcher_resume_uploads",
    )

    if resume_files:
        st.caption(f"{len(resume_files)} resume(s) uploaded")
        for resume_file in resume_files:
            st.write(f"• {resume_file.name}")

    st.divider()

    # --------------------------------------------------------
    # STEP 3 — MATCH
    # --------------------------------------------------------

    st.header("3. Candidate Matching")

    match_button = st.button(
        "Analyse & Rank Candidates",
        type="primary",
        use_container_width=True,
        key="matcher_run_button",
    )

    if not match_button:
        return

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not designation.strip():
        st.error("Please enter the job designation.")
        return

    if jd_file is None:
        st.error("Please upload a job description.")
        return

    if not resume_files:
        st.error("Please upload at least one candidate resume.")
        return

    total_start = time.perf_counter()

    status_box = st.status(
        "Starting JD candidate matching...",
        expanded=True,
    )

    try:
        # ====================================================
        # STEP 1 — EXTRACT COMPLETE JD TEXT
        # ====================================================

        status_box.write("1. Extracting complete JD text...")

        jd_text = extract_uploaded_document(jd_file)

        if not jd_text:
            raise ValueError("No text could be extracted from the JD.")

        status_box.write(
            f"✓ JD extracted ({len(jd_text):,} characters)"
        )

        # ====================================================
        # STEP 2 — EMBED + SAVE JD
        # ====================================================

        status_box.write("2. Creating JD embedding and saving JD...")

        jd_data = create_and_save_jd(
            designation=designation,
            jd_text=jd_text,
        )

        jd_embedding = jd_data["embedding"]

        status_box.write(
            f"✓ JD saved to database as row {jd_data['id']}"
        )

        # ====================================================
        # STEP 3 — EXTRACT ALL RESUMES
        # ====================================================

        status_box.write("3. Extracting candidate resume text...")

        resumes = []
        skipped_files = []

        for resume_file in resume_files:
            try:
                resume_text = extract_uploaded_document(resume_file)

                if not resume_text:
                    skipped_files.append(resume_file.name)
                    continue

                resumes.append(
                    {
                        "name": resume_file.name,
                        "text": resume_text,
                    }
                )

                status_box.write(
                    f"✓ Extracted {resume_file.name}"
                )

            except Exception as exc:
                logger.exception(
                    "Could not extract resume: %s",
                    resume_file.name,
                )
                skipped_files.append(resume_file.name)
                status_box.write(
                    f"⚠ Could not read {resume_file.name}: {exc}"
                )

        if not resumes:
            raise ValueError(
                "No usable text could be extracted from the uploaded resumes."
            )

        # ====================================================
        # STEP 4 — EMBED + COSINE MATCH
        # ====================================================

        status_box.write(
            "4. Creating resume embeddings and calculating similarity..."
        )

        results = match_uploaded_resumes(
            jd_embedding=jd_embedding,
            resumes=resumes,
        )

        if not results:
            raise ValueError("No candidates could be matched.")

        total_elapsed = time.perf_counter() - total_start

        status_box.update(
            label=(
                f"Matching completed for {len(results)} candidate(s) "
                f"in {total_elapsed:.1f}s"
            ),
            state="complete",
            expanded=False,
        )

        # ====================================================
        # RESULTS
        # ====================================================

        st.success(
            f"Matched {len(results)} candidate(s) against "
            f"{designation.strip()}."
        )

        st.divider()
        st.header("🏆 Ranked Candidates")

        top_candidate = results[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Top Candidate",
                top_candidate["Candidate"],
            )

        with col2:
            st.metric(
                "Similarity Score",
                f"{top_candidate['Match Score']:.4f}",
            )

        with col3:
            st.metric(
                "Candidates Matched",
                len(results),
            )

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Match Score is cosine similarity between the complete JD "
            "embedding and the complete resume embedding. It should not "
            "yet be interpreted as a qualification percentage."
        )

        if skipped_files:
            st.warning(
                "Skipped files: " + ", ".join(skipped_files)
            )

        with st.expander(
            "View Processed Job Description",
            expanded=False,
        ):
            st.write(f"**Designation:** {designation.strip()}")
            st.write(f"**Database row:** {jd_data['id']}")
            st.text_area(
                "Extracted JD Text",
                jd_text,
                height=350,
                disabled=True,
                key="matcher_extracted_jd_text",
            )

        with st.expander(
            "Developer View — Matching Results",
            expanded=False,
        ):
            st.json(
                {
                    "jd_id": jd_data["id"],
                    "designation": designation.strip(),
                    "embedding_dimensions": len(jd_embedding),
                    "results": results,
                    "skipped_files": skipped_files,
                }
            )

    except Exception as exc:
        total_elapsed = time.perf_counter() - total_start

        logger.exception(
            "JD candidate matching failed after %.2f seconds.",
            total_elapsed,
        )

        status_box.update(
            label="JD candidate matching failed",
            state="error",
            expanded=True,
        )

        st.error("JD candidate matching failed.")
        st.exception(exc)


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Candidate Benchmark",
        "🎯 JD Candidate Matcher",
    ],
)

if page == "📊 Candidate Benchmark":
    show_candidate_benchmark()
else:
    show_jd_candidate_matcher()
