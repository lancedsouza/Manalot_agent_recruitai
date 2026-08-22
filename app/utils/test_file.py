# # import os
# # import time
# # from pathlib import Path

# # from dotenv import load_dotenv
# # import instructor
# # import pdfplumber
# # from openai import OpenAI

# # from app.db.save_candidate import save_resume_to_db
# # from app.models.resume import Resume
# # from app.utils.ground_truth import GROUND_TRUTH_DATA

# # from app.utils.section_extractor import (
# #     extract_experience_section,
# #     extract_education_section,
# #     extract_name_section,
# # )


# # # ============================================================
# # # CONFIGURATION
# # # ============================================================

# # MODEL_NAME = "llama-3.1-8b-instant"
# # FOLDER_PATH = Path(
# #     "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/"
# #     "Medline/Sr.Mgr FP&A/test"
# # )


# # # ============================================================
# # # LOAD .ENV
# # # ============================================================

# # # ENV_PATH = Path(__file__).resolve().parent / ".env"
# # ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
# # load_dotenv(ENV_PATH)

# # api_key = os.getenv("GROQ_API_KEY")

# # BASE_URL = "https://api.groq.com/openai/v1"


# # print("=" * 70)
# # print("PROVIDER CONFIGURATION")
# # print("=" * 70)

# # print("Provider : Groq")
# # print(f"Model    : {MODEL_NAME}")
# # print(f"API key  : {'YES' if api_key else 'NO'}")
# # print(f".env     : {ENV_PATH}")

# # print("=" * 70)


# # if not api_key:
# #     raise ValueError(
# #         f"GROQ_API_KEY not found in {ENV_PATH}"
# #     )


# # # ============================================================
# # # GROQ + INSTRUCTOR
# # # ============================================================

# # client = instructor.from_openai(
# #     OpenAI(
# #         api_key=api_key,
# #         base_url=BASE_URL,
# #     ),
# #     mode=instructor.Mode.JSON,
# # )


# # # ============================================================
# # # NORMALIZATION
# # # ============================================================

# # def normalize_name(name: str) -> str:

# #     if not name:
# #         return ""

# #     return " ".join(
# #         name.upper().split()
# #     )


# # def normalize_skill(skill: str) -> str:

# #     if not skill:
# #         return ""

# #     return " ".join(
# #         skill.upper().split()
# #     )


# # NORMALIZED_GROUND_TRUTH = {
# #     normalize_name(name): skills
# #     for name, skills in GROUND_TRUTH_DATA.items()
# # }


# # # ============================================================
# # # GROUND TRUTH
# # # ============================================================

# # def get_ground_truth_skills(name: str):

# #     normalized_name = normalize_name(name)

# #     if not normalized_name:
# #         return None

# #     skills = NORMALIZED_GROUND_TRUTH.get(
# #         normalized_name
# #     )

# #     if skills is None:

# #         print()
# #         print(
# #             f"WARNING: No ground truth found "
# #             f"for candidate: {name}"
# #         )

# #         return None

# #     return skills


# # # ============================================================
# # # PDF EXTRACTION
# # # ============================================================

# # def extract_text(file_path: Path) -> str:

# #     start = time.time()

# #     path = Path(file_path)

# #     if not path.exists():

# #         raise FileNotFoundError(
# #             f"PDF not found: {file_path}"
# #         )

# #     extracted_text = []

# #     with pdfplumber.open(path) as pdf:

# #         for page in pdf.pages:

# #             page_text = page.extract_text()

# #             if page_text:

# #                 extracted_text.append(
# #                     page_text
# #                 )

# #     elapsed = time.time() - start

# #     print(
# #         f"PDF extraction time: "
# #         f"{elapsed:.2f} seconds"
# #     )

# #     return "\n\n".join(
# #         extracted_text
# #     )


# # # ============================================================
# # # LLM EXTRACTION
# # # ============================================================

# # def parse_resume_to_pydantic(
# #     candidate_name: str,
# #     experience_text: str,
# #     education_text: str,
# # ) -> Resume:

# #     start = time.time()

# #     if (
# #         not experience_text.strip()
# #         and not education_text.strip()
# #     ):

# #         print(
# #             "No experience or education text available."
# #         )

# #         return Resume(
# #             name=candidate_name,
# #             experience_years=0.0,
# #         )

# #     prompt = f"""
# # CURRENT DATE:
# # August 2026

# # CANDIDATE NAME:
# # {candidate_name}

# # ========================
# # EXPERIENCE SECTION
# # ========================

# # {experience_text}

# # ========================
# # EDUCATION SECTION
# # ========================

# # {education_text}
# # """

# #     response = client.chat.completions.create(

# #         model=MODEL_NAME,

# #         response_model=Resume,

# #         max_retries=1,

# #         messages=[

# #             {
# #                 "role": "system",

# #                 "content": """
# # You are an expert technical recruiter and
# # resume information extraction system.

# # Extract structured information from the
# # provided resume sections.

# # IMPORTANT:

# # Skills must be extracted or clearly inferred
# # ONLY from the EXPERIENCE SECTION.

# # Do not derive skills from education.


# # ================================================
# # 1. NAME
# # ================================================

# # Use the supplied candidate name exactly.

# # Populate the name field.


# # ================================================
# # 2. EXPERIENCE
# # ================================================

# # Extract EVERY clearly identifiable professional
# # employment record.

# # For each experience extract:

# # - company
# # - title
# # - start_date
# # - end_date

# # Do not invent dates.

# # Normalize dates where possible.

# # Examples:

# # Nov-2020 -> Nov 2020
# # Jan-18 -> Jan 2018
# # Sept 2015 -> Sep 2015

# # If the resume says:

# # Present
# # Current
# # Till Date
# # To Date

# # treat it as current employment.


# # ================================================
# # 3. TOTAL PROFESSIONAL EXPERIENCE
# # ================================================

# # AFTER extracting all employment records,
# # calculate experience_years using the extracted
# # employment dates.

# # Follow these steps carefully:

# # 1. Identify the earliest professional
# #    employment start date.

# # 2. Identify the latest employment end date.

# # 3. Treat:
# #    Current
# #    Present
# #    Till Date
# #    To Date

# #    as August 2026.

# # 4. Examine ALL employment periods for gaps.

# # 5. Do NOT double-count overlapping periods.

# # 6. If one role ends during the same month
# #    another begins, treat the employment
# #    history as continuous.

# # 7. Calculate the total ACTUAL employed
# #    duration.

# # 8. Do NOT estimate experience based on:
# #    - title
# #    - seniority
# #    - summary
# #    - age
# #    - number of jobs

# # 9. Return experience_years as a decimal.

# # Examples:

# # 15 years = 15.0

# # 15 years 6 months = 15.5

# # 10 years 3 months = 10.25

# # Before returning the result, verify that
# # experience_years is mathematically consistent
# # with ALL extracted employment dates.

# # The experience_years field MUST be populated.


# # ================================================
# # 4. SKILLS
# # ================================================

# # Extract ALL professional skills that are
# # explicitly stated or clearly demonstrated
# # in the EXPERIENCE SECTION.

# # Include:

# # - technologies
# # - tools
# # - software
# # - platforms
# # - programming languages
# # - frameworks
# # - databases
# # - finance skills
# # - accounting skills
# # - business domains
# # - analytical skills
# # - methodologies
# # - processes
# # - professional competencies

# # Examples:

# # FP&A
# # Financial Planning
# # Budgeting
# # Forecasting
# # Financial Modeling
# # Variance Analysis
# # SAP
# # SAP S/4 HANA
# # Oracle
# # Power BI
# # Python
# # RPA
# # AI
# # IFRS
# # US GAAP
# # SOX
# # Process Improvement
# # Financial Reporting

# # Do NOT include:

# # - company names
# # - job titles
# # - candidate names
# # - degrees
# # - generic words
# # - unsupported skills

# # Be comprehensive.

# # If a professional skill appears only once
# # in the experience text, still include it.

# # Do not limit the number of skills.


# # ================================================
# # 5. EDUCATION
# # ================================================

# # Extract every clearly identifiable
# # education record.

# # For each record extract:

# # - degree
# # - institution
# # - start_date
# # - end_date

# # Do not invent missing information.


# # ================================================
# # 6. FINAL RULE
# # ================================================

# # Only return information supported by
# # the supplied resume sections.

# # Return data matching the requested
# # Pydantic schema.
# # """
# #             },

# #             {
# #                 "role": "user",
# #                 "content": prompt,
# #             },
# #         ],
# #     )

# #     elapsed = time.time() - start

# #     print(
# #         f"LLM extraction time: "
# #         f"{elapsed:.2f} seconds"
# #     )

# #     return response


# # # ============================================================
# # # PRECISION / RECALL / F1
# # # ============================================================

# # def precision_test(
# #     ground_truth,
# #     extracted_skills,
# # ):

# #     ground_truth_set = {
# #         normalize_skill(skill)
# #         for skill in ground_truth
# #         if skill
# #     }

# #     extracted_skills_set = {
# #         normalize_skill(skill)
# #         for skill in extracted_skills
# #         if skill
# #     }

# #     true_positives = (
# #         ground_truth_set
# #         & extracted_skills_set
# #     )

# #     false_positives = (
# #         extracted_skills_set
# #         - ground_truth_set
# #     )

# #     false_negatives = (
# #         ground_truth_set
# #         - extracted_skills_set
# #     )

# #     precision_denominator = (
# #         len(true_positives)
# #         + len(false_positives)
# #     )

# #     recall_denominator = (
# #         len(true_positives)
# #         + len(false_negatives)
# #     )

# #     precision = (
# #         len(true_positives)
# #         / precision_denominator
# #         if precision_denominator > 0
# #         else 0
# #     )

# #     recall = (
# #         len(true_positives)
# #         / recall_denominator
# #         if recall_denominator > 0
# #         else 0
# #     )

# #     f1_score = (
# #         2 * precision * recall
# #         / (precision + recall)
# #         if precision + recall > 0
# #         else 0
# #     )

# #     return (
# #         precision,
# #         recall,
# #         f1_score,
# #         true_positives,
# #         false_positives,
# #         false_negatives,
# #     )


# # # ============================================================
# # # MAIN
# # # ============================================================

# # def main():

# #     pdf_files = list(
# #         FOLDER_PATH.glob("*.pdf")
# #     )

# #     print()
# #     print(
# #         f"Found {len(pdf_files)} PDF files."
# #     )

# #     total_true_positives = 0
# #     total_false_positives = 0
# #     total_false_negatives = 0

# #     evaluated_resumes = 0
# #     skipped_resumes = 0


# #     # ========================================================
# #     # PROCESS EACH PDF
# #     # ========================================================

# #     for file in pdf_files:

# #         print()
# #         print("=" * 70)

# #         print(
# #             f"Processing: {file.name}"
# #         )

# #         print("=" * 70)

# #         try:

# #             # ==================================================
# #             # STEP 1 — EXTRACT PDF TEXT
# #             # ==================================================

# #             full_text = extract_text(
# #                 file
# #             )

# #             print(
# #                 f"Extracted characters: "
# #                 f"{len(full_text)}"
# #             )

# #             if not full_text.strip():

# #                 print(
# #                     "No text extracted."
# #                 )

# #                 continue


# #             # ==================================================
# #             # STEP 2 — NAME
# #             # ==================================================

# #             name = extract_name_section(
# #                 full_text
# #             )

# #             print(
# #                 f"Candidate: {name}"
# #             )


# #             # ==================================================
# #             # STEP 3 — EXPERIENCE SECTION
# #             # ==================================================

# #             experience_section = (
# #                 extract_experience_section(
# #                     full_text
# #                 )
# #             )

# #             print(
# #                 f"Experience characters: "
# #                 f"{len(experience_section)}"
# #             )


# #             # ==================================================
# #             # STEP 4 — EDUCATION SECTION
# #             # ==================================================

# #             education_section = (
# #                 extract_education_section(
# #                     full_text
# #                 )
# #             )

# #             print(
# #                 f"Education characters: "
# #                 f"{len(education_section)}"
# #             )


# #             # ==================================================
# #             # STEP 5 — LLM → PYDANTIC
# #             # ==================================================

# #             print()
# #             print(
# #                 "Sending experience + education "
# #                 "to LLM..."
# #             )

# #             llm_results = (
# #                 parse_resume_to_pydantic(
# #                     candidate_name=name,
# #                     experience_text=experience_section,
# #                     education_text=education_section,
# #                 )
# #             )


# #             # ==================================================
# #             # IMPORTANT:
# #             # GUARANTEE NAME FROM DETERMINISTIC EXTRACTOR
# #             # ==================================================

# #             llm_results.name = name


# #             # ==================================================
# #             # STEP 6 — SAVE TO POSTGRESQL
# #             # ==================================================

# #             print()
# #             print(
# #                 "Saving candidate to PostgreSQL..."
# #             )

# #             saved_candidate = (
# #                 save_resume_to_db(
# #                     resume=llm_results,
# #                     resume_text=full_text,
# #                 )
# #             )


# #             print()
# #             print("-" * 70)
# #             print("DATABASE RESULT")
# #             print("-" * 70)

# #             print(
# #                 f"Database ID: "
# #                 f"{saved_candidate.id}"
# #             )

# #             print(
# #                 f"Saved Name: "
# #                 f"{saved_candidate.name}"
# #             )

# #             print(
# #                 f"Saved Experience Years: "
# #                 f"{saved_candidate.experience_years}"
# #             )

# #             print(
# #                 f"Saved Skills: "
# #                 f"{len(saved_candidate.skills or [])}"
# #             )


# #             # ==================================================
# #             # STEP 7 — DISPLAY EXTRACTED RESUME
# #             # ==================================================

# #             print()
# #             print("-" * 70)
# #             print("EXTRACTED RESUME")
# #             print("-" * 70)

# #             print()

# #             print(
# #                 f"Candidate: "
# #                 f"{llm_results.name}"
# #             )

# #             print()

# #             print(
# #                 "Experience Years:"
# #             )

# #             print(
# #                 llm_results.experience_years
# #             )

# #             print()

# #             print(
# #                 "Extracted Skills:"
# #             )

# #             print(
# #                 llm_results.skills
# #             )

# #             print()

# #             print(
# #                 "Experience:"
# #             )

# #             print(
# #                 llm_results.experience
# #             )

# #             print()

# #             print(
# #                 "Education:"
# #             )

# #             print(
# #                 llm_results.education
# #             )


# #             # ==================================================
# #             # STEP 8 — OPTIONAL EVALUATION
# #             # ==================================================

# #             ground_truth_skills = (
# #                 get_ground_truth_skills(
# #                     name
# #                 )
# #             )

# #             if ground_truth_skills is None:

# #                 skipped_resumes += 1

# #                 print()
# #                 print(
# #                     "Ground truth unavailable. "
# #                     "Skipping evaluation."
# #                 )

# #                 continue


# #             (
# #                 precision,
# #                 recall,
# #                 f1_score,
# #                 true_positives,
# #                 false_positives,
# #                 false_negatives,
# #             ) = precision_test(
# #                 ground_truth_skills,
# #                 llm_results.skills,
# #             )


# #             total_true_positives += (
# #                 len(true_positives)
# #             )

# #             total_false_positives += (
# #                 len(false_positives)
# #             )

# #             total_false_negatives += (
# #                 len(false_negatives)
# #             )

# #             evaluated_resumes += 1


# #             # ==================================================
# #             # PRINT EVALUATION
# #             # ==================================================

# #             print()
# #             print("=" * 70)
# #             print("RESULT")
# #             print("=" * 70)

# #             print()
# #             print(
# #                 f"Candidate: {name}"
# #             )

# #             print()

# #             print(
# #                 "Ground Truth Skills:"
# #             )

# #             print(
# #                 ground_truth_skills
# #             )

# #             print()

# #             print(
# #                 "Extracted Skills:"
# #             )

# #             print(
# #                 llm_results.skills
# #             )

# #             print()

# #             print(
# #                 f"True Positives  : "
# #                 f"{len(true_positives)}"
# #             )

# #             print(
# #                 f"False Positives : "
# #                 f"{len(false_positives)}"
# #             )

# #             print(
# #                 f"False Negatives : "
# #                 f"{len(false_negatives)}"
# #             )

# #             print()

# #             print(
# #                 f"Precision       : "
# #                 f"{precision:.2f}"
# #             )

# #             print(
# #                 f"Recall          : "
# #                 f"{recall:.2f}"
# #             )

# #             print(
# #                 f"F1 Score        : "
# #                 f"{f1_score:.2f}"
# #             )

# #             print()

# #             print(
# #                 "Matched Skills:"
# #             )

# #             print(
# #                 sorted(
# #                     true_positives
# #                 )
# #             )

# #             print()

# #             print(
# #                 "Missing Skills:"
# #             )

# #             print(
# #                 sorted(
# #                     false_negatives
# #                 )
# #             )

# #             print()

# #             print(
# #                 "Extra Skills:"
# #             )

# #             print(
# #                 sorted(
# #                     false_positives
# #                 )
# #             )


# #         except Exception as e:

# #             print()
# #             print(
# #                 f"ERROR processing "
# #                 f"{file.name}"
# #             )

# #             print(
# #                 repr(e)
# #             )

# #             continue


# #     # ========================================================
# #     # OVERALL EVALUATION
# #     # ========================================================

# #     print()
# #     print()
# #     print("=" * 70)
# #     print("OVERALL EVALUATION")
# #     print("=" * 70)

# #     print()

# #     print(
# #         f"Resumes evaluated : "
# #         f"{evaluated_resumes}"
# #     )

# #     print(
# #         f"Resumes skipped   : "
# #         f"{skipped_resumes}"
# #     )


# #     precision_denominator = (
# #         total_true_positives
# #         + total_false_positives
# #     )

# #     recall_denominator = (
# #         total_true_positives
# #         + total_false_negatives
# #     )


# #     overall_precision = (
# #         total_true_positives
# #         / precision_denominator
# #         if precision_denominator > 0
# #         else 0
# #     )

# #     overall_recall = (
# #         total_true_positives
# #         / recall_denominator
# #         if recall_denominator > 0
# #         else 0
# #     )

# #     overall_f1 = (
# #         2
# #         * overall_precision
# #         * overall_recall
# #         / (
# #             overall_precision
# #             + overall_recall
# #         )
# #         if (
# #             overall_precision
# #             + overall_recall
# #         ) > 0
# #         else 0
# #     )


# #     print()

# #     print(
# #         f"Total True Positives  : "
# #         f"{total_true_positives}"
# #     )

# #     print(
# #         f"Total False Positives : "
# #         f"{total_false_positives}"
# #     )

# #     print(
# #         f"Total False Negatives : "
# #         f"{total_false_negatives}"
# #     )

# #     print()

# #     print(
# #         f"Overall Precision     : "
# #         f"{overall_precision:.2f}"
# #     )

# #     print(
# #         f"Overall Recall        : "
# #         f"{overall_recall:.2f}"
# #     )

# #     print(
# #         f"Overall F1 Score      : "
# #         f"{overall_f1:.2f}"
# #     )

# #     print()
# #     print("=" * 70)


# # # ============================================================
# # # ENTRY POINT
# # # ============================================================

# # if __name__ == "__main__":
# #     main()

# """code with local llm"""
# # import time
# # from pathlib import Path

# # import instructor
# # import pdfplumber

# # from app.db.save_candidate import save_resume_to_db
# # from app.models.resume import Resume
# # from app.utils.ground_truth import GROUND_TRUTH_DATA

# # from app.utils.section_extractor import (
# #     extract_experience_section,
# #     extract_education_section,
# #     extract_name_section,
# # )


# # # ============================================================
# # # CONFIGURATION
# # # ============================================================

# # MODEL_NAME = "qwen2.5:3b"

# # FOLDER_PATH = Path(
# #     "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/"
# #     "Medline/Sr.Mgr FP&A/test"
# # )


# # # ============================================================
# # # LOCAL OLLAMA + INSTRUCTOR
# # # ============================================================

# # print("=" * 70)
# # print("PROVIDER CONFIGURATION")
# # print("=" * 70)

# # print("Provider : Ollama (LOCAL)")
# # print(f"Model    : {MODEL_NAME}")
# # print("Server   : http://localhost:11434")

# # print("=" * 70)


# # client = instructor.from_provider(
# #     f"ollama/{MODEL_NAME}",
# #     base_url="http://localhost:11434/v1",
# #     mode=instructor.Mode.JSON,
# # )


# # # ============================================================
# # # NORMALIZATION
# # # ============================================================

# # def normalize_name(name: str) -> str:

# #     if not name:
# #         return ""

# #     return " ".join(
# #         name.upper().split()
# #     )


# # def normalize_skill(skill: str) -> str:

# #     if not skill:
# #         return ""

# #     return " ".join(
# #         skill.upper().split()
# #     )


# # NORMALIZED_GROUND_TRUTH = {
# #     normalize_name(name): skills
# #     for name, skills in GROUND_TRUTH_DATA.items()
# # }


# # # ============================================================
# # # GROUND TRUTH
# # # ============================================================

# # def get_ground_truth_skills(name: str):

# #     normalized_name = normalize_name(name)

# #     if not normalized_name:
# #         return None

# #     skills = NORMALIZED_GROUND_TRUTH.get(
# #         normalized_name
# #     )

# #     if skills is None:

# #         print()
# #         print(
# #             f"WARNING: No ground truth found "
# #             f"for candidate: {name}"
# #         )

# #         return None

# #     return skills


# # # ============================================================
# # # PDF EXTRACTION
# # # ============================================================

# # def extract_text(file_path: Path) -> str:

# #     start = time.time()

# #     path = Path(file_path)

# #     if not path.exists():

# #         raise FileNotFoundError(
# #             f"PDF not found: {file_path}"
# #         )

# #     extracted_text = []

# #     with pdfplumber.open(path) as pdf:

# #         for page in pdf.pages:

# #             page_text = page.extract_text()

# #             if page_text:

# #                 extracted_text.append(
# #                     page_text
# #                 )

# #     elapsed = time.time() - start

# #     print(
# #         f"PDF extraction time: "
# #         f"{elapsed:.2f} seconds"
# #     )

# #     return "\n\n".join(
# #         extracted_text
# #     )


# # # ============================================================
# # # LOCAL LLM EXTRACTION
# # # ============================================================

# # def parse_resume_to_pydantic(
# #     candidate_name: str,
# #     experience_text: str,
# #     education_text: str,
# # ) -> Resume:

# #     start = time.time()

# #     if (
# #         not experience_text.strip()
# #         and not education_text.strip()
# #     ):

# #         print(
# #             "No experience or education text available."
# #         )

# #         return Resume(
# #             name=candidate_name,
# #             experience_years=0.0,
# #         )


# #     prompt = f"""
# # CURRENT DATE:
# # August 2026

# # CANDIDATE NAME:
# # {candidate_name}

# # ========================
# # EXPERIENCE SECTION
# # ========================

# # {experience_text}

# # ========================
# # EDUCATION SECTION
# # ========================

# # {education_text}
# # """


# #     response = client.create(

# #         response_model=Resume,

# #         max_retries=2,

# #         messages=[

# #             {
# #                 "role": "system",

# #                 "content": """
# # You are an expert technical recruiter and
# # resume information extraction system.

# # Extract structured information from the
# # provided resume sections.

# # IMPORTANT:

# # Skills must be extracted or clearly inferred
# # ONLY from the EXPERIENCE SECTION.

# # Do not derive skills from education.


# # ================================================
# # 1. NAME
# # ================================================

# # Use the supplied candidate name exactly.

# # Populate the name field.


# # ================================================
# # 2. EXPERIENCE
# # ================================================

# # Extract EVERY clearly identifiable professional
# # employment record.

# # For each experience extract:

# # - company
# # - title
# # - start_date
# # - end_date

# # Do not invent dates.

# # Normalize dates where possible.

# # Examples:

# # Nov-2020 -> Nov 2020
# # Jan-18 -> Jan 2018
# # Sept 2015 -> Sep 2015

# # If the resume says:

# # Present
# # Current
# # Till Date
# # To Date

# # treat it as current employment.


# # ================================================
# # 3. TOTAL PROFESSIONAL EXPERIENCE
# # ================================================

# # AFTER extracting all employment records,
# # calculate experience_years using the extracted
# # employment dates.

# # Follow these steps carefully:

# # 1. Identify the earliest professional
# #    employment start date.

# # 2. Identify the latest employment end date.

# # 3. Treat:
# #    Current
# #    Present
# #    Till Date
# #    To Date

# #    as August 2026.

# # 4. Examine ALL employment periods for gaps.

# # 5. Do NOT double-count overlapping periods.

# # 6. If one role ends during the same month
# #    another begins, treat the employment
# #    history as continuous.

# # 7. Calculate the total ACTUAL employed
# #    duration.

# # 8. Do NOT estimate experience based on:
# #    - title
# #    - seniority
# #    - summary
# #    - age
# #    - number of jobs

# # 9. Return experience_years as a decimal.

# # Examples:

# # 15 years = 15.0

# # 15 years 6 months = 15.5

# # 10 years 3 months = 10.25

# # Before returning the result, verify that
# # experience_years is mathematically consistent
# # with ALL extracted employment dates.

# # The experience_years field MUST be populated.


# # ================================================
# # 4. SKILLS
# # ================================================

# # Extract ALL professional skills that are
# # explicitly stated or clearly demonstrated
# # in the EXPERIENCE SECTION.

# # Include:

# # - technologies
# # - tools
# # - software
# # - platforms
# # - programming languages
# # - frameworks
# # - databases
# # - finance skills
# # - accounting skills
# # - business domains
# # - analytical skills
# # - methodologies
# # - processes
# # - professional competencies

# # Examples:

# # FP&A
# # Financial Planning
# # Budgeting
# # Forecasting
# # Financial Modeling
# # Variance Analysis
# # SAP
# # SAP S/4 HANA
# # Oracle
# # Power BI
# # Python
# # RPA
# # AI
# # IFRS
# # US GAAP
# # SOX
# # Process Improvement
# # Financial Reporting

# # Do NOT include:

# # - company names
# # - job titles
# # - candidate names
# # - degrees
# # - generic words
# # - unsupported skills

# # Be comprehensive.

# # If a professional skill appears only once
# # in the experience text, still include it.

# # Do not limit the number of skills.


# # ================================================
# # 5. EDUCATION
# # ================================================

# # Extract every clearly identifiable
# # education record.

# # For each record extract:

# # - degree
# # - institution
# # - start_date
# # - end_date

# # Do not invent missing information.


# # ================================================
# # 6. FINAL RULE
# # ================================================

# # Only return information supported by
# # the supplied resume sections.

# # Return data matching the requested
# # Pydantic schema.
# # """
# #             },

# #             {
# #                 "role": "user",
# #                 "content": prompt,
# #             },
# #         ],
# #     )


# #     elapsed = time.time() - start

# #     print(
# #         f"Local LLM extraction time: "
# #         f"{elapsed:.2f} seconds"
# #     )

# #     return response


# # # ============================================================
# # # PRECISION / RECALL / F1
# # # ============================================================

# # def precision_test(
# #     ground_truth,
# #     extracted_skills,
# # ):

# #     ground_truth_set = {
# #         normalize_skill(skill)
# #         for skill in ground_truth
# #         if skill
# #     }

# #     extracted_skills_set = {
# #         normalize_skill(skill)
# #         for skill in extracted_skills
# #         if skill
# #     }


# #     true_positives = (
# #         ground_truth_set
# #         & extracted_skills_set
# #     )


# #     false_positives = (
# #         extracted_skills_set
# #         - ground_truth_set
# #     )


# #     false_negatives = (
# #         ground_truth_set
# #         - extracted_skills_set
# #     )


# #     precision_denominator = (
# #         len(true_positives)
# #         + len(false_positives)
# #     )


# #     recall_denominator = (
# #         len(true_positives)
# #         + len(false_negatives)
# #     )


# #     precision = (
# #         len(true_positives)
# #         / precision_denominator
# #         if precision_denominator > 0
# #         else 0
# #     )


# #     recall = (
# #         len(true_positives)
# #         / recall_denominator
# #         if recall_denominator > 0
# #         else 0
# #     )


# #     f1_score = (
# #         2 * precision * recall
# #         / (precision + recall)
# #         if precision + recall > 0
# #         else 0
# #     )


# #     return (
# #         precision,
# #         recall,
# #         f1_score,
# #         true_positives,
# #         false_positives,
# #         false_negatives,
# #     )


# # # ============================================================
# # # MAIN
# # # ============================================================

# # def main():

# #     pdf_files = list(
# #         FOLDER_PATH.glob("*.pdf")
# #     )


# #     print()

# #     print(
# #         f"Found {len(pdf_files)} PDF files."
# #     )


# #     total_true_positives = 0
# #     total_false_positives = 0
# #     total_false_negatives = 0

# #     evaluated_resumes = 0
# #     skipped_resumes = 0


# #     # ========================================================
# #     # PROCESS EACH PDF
# #     # ========================================================

# #     for file in pdf_files:

# #         print()
# #         print("=" * 70)

# #         print(
# #             f"Processing: {file.name}"
# #         )

# #         print("=" * 70)


# #         try:

# #             # ==================================================
# #             # STEP 1 — EXTRACT PDF TEXT
# #             # ==================================================

# #             full_text = extract_text(
# #                 file
# #             )


# #             print(
# #                 f"Extracted characters: "
# #                 f"{len(full_text)}"
# #             )


# #             if not full_text.strip():

# #                 print(
# #                     "No text extracted."
# #                 )

# #                 continue


# #             # ==================================================
# #             # STEP 2 — NAME
# #             # ==================================================

# #             name = extract_name_section(
# #                 full_text
# #             )


# #             print(
# #                 f"Candidate: {name}"
# #             )


# #             # ==================================================
# #             # STEP 3 — EXPERIENCE SECTION
# #             # ==================================================

# #             experience_section = (
# #                 extract_experience_section(
# #                     full_text
# #                 )
# #             )


# #             print(
# #                 f"Experience characters: "
# #                 f"{len(experience_section)}"
# #             )


# #             # ==================================================
# #             # STEP 4 — EDUCATION SECTION
# #             # ==================================================

# #             education_section = (
# #                 extract_education_section(
# #                     full_text
# #                 )
# #             )


# #             print(
# #                 f"Education characters: "
# #                 f"{len(education_section)}"
# #             )


# #             # ==================================================
# #             # STEP 5 — LOCAL QWEN → PYDANTIC
# #             # ==================================================

# #             print()

# #             print(
# #                 "Sending experience + education "
# #                 "to LOCAL Qwen..."
# #             )


# #             llm_results = (
# #                 parse_resume_to_pydantic(
# #                     candidate_name=name,
# #                     experience_text=experience_section,
# #                     education_text=education_section,
# #                 )
# #             )


# #             # ==================================================
# #             # GUARANTEE NAME FROM DETERMINISTIC EXTRACTOR
# #             # ==================================================

# #             llm_results.name = name


# #             # ==================================================
# #             # STEP 6 — SAVE TO POSTGRESQL
# #             # ==================================================

# #             print()

# #             print(
# #                 "Saving candidate to PostgreSQL..."
# #             )


# #             saved_candidate = (
# #                 save_resume_to_db(
# #                     resume=llm_results,
# #                     resume_text=full_text,
# #                 )
# #             )


# #             print()
# #             print("-" * 70)
# #             print("DATABASE RESULT")
# #             print("-" * 70)


# #             print(
# #                 f"Database ID: "
# #                 f"{saved_candidate.id}"
# #             )


# #             print(
# #                 f"Saved Name: "
# #                 f"{saved_candidate.name}"
# #             )


# #             print(
# #                 f"Saved Experience Years: "
# #                 f"{saved_candidate.experience_years}"
# #             )


# #             print(
# #                 f"Saved Skills: "
# #                 f"{len(saved_candidate.skills or [])}"
# #             )


# #             # ==================================================
# #             # STEP 7 — DISPLAY EXTRACTED RESUME
# #             # ==================================================

# #             print()
# #             print("-" * 70)
# #             print("EXTRACTED RESUME")
# #             print("-" * 70)

# #             print()

# #             print(
# #                 f"Candidate: "
# #                 f"{llm_results.name}"
# #             )

# #             print()

# #             print(
# #                 "Experience Years:"
# #             )

# #             print(
# #                 llm_results.experience_years
# #             )

# #             print()

# #             print(
# #                 "Extracted Skills:"
# #             )

# #             print(
# #                 llm_results.skills
# #             )

# #             print()

# #             print(
# #                 "Experience:"
# #             )

# #             print(
# #                 llm_results.experience
# #             )

# #             print()

# #             print(
# #                 "Education:"
# #             )

# #             print(
# #                 llm_results.education
# #             )


# #             # ==================================================
# #             # STEP 8 — OPTIONAL EVALUATION
# #             # ==================================================

# #             ground_truth_skills = (
# #                 get_ground_truth_skills(
# #                     name
# #                 )
# #             )


# #             if ground_truth_skills is None:

# #                 skipped_resumes += 1

# #                 print()

# #                 print(
# #                     "Ground truth unavailable. "
# #                     "Skipping evaluation."
# #                 )

# #                 continue


# #             (
# #                 precision,
# #                 recall,
# #                 f1_score,
# #                 true_positives,
# #                 false_positives,
# #                 false_negatives,
# #             ) = precision_test(
# #                 ground_truth_skills,
# #                 llm_results.skills,
# #             )


# #             total_true_positives += (
# #                 len(true_positives)
# #             )

# #             total_false_positives += (
# #                 len(false_positives)
# #             )

# #             total_false_negatives += (
# #                 len(false_negatives)
# #             )

# #             evaluated_resumes += 1


# #             # ==================================================
# #             # PRINT EVALUATION
# #             # ==================================================

# #             print()
# #             print("=" * 70)
# #             print("RESULT")
# #             print("=" * 70)

# #             print()

# #             print(
# #                 f"Candidate: {name}"
# #             )

# #             print()

# #             print(
# #                 "Ground Truth Skills:"
# #             )

# #             print(
# #                 ground_truth_skills
# #             )

# #             print()

# #             print(
# #                 "Extracted Skills:"
# #             )

# #             print(
# #                 llm_results.skills
# #             )

# #             print()

# #             print(
# #                 f"True Positives  : "
# #                 f"{len(true_positives)}"
# #             )

# #             print(
# #                 f"False Positives : "
# #                 f"{len(false_positives)}"
# #             )

# #             print(
# #                 f"False Negatives : "
# #                 f"{len(false_negatives)}"
# #             )

# #             print()

# #             print(
# #                 f"Precision       : "
# #                 f"{precision:.2f}"
# #             )

# #             print(
# #                 f"Recall          : "
# #                 f"{recall:.2f}"
# #             )

# #             print(
# #                 f"F1 Score        : "
# #                 f"{f1_score:.2f}"
# #             )

# #             print()

# #             print(
# #                 "Matched Skills:"
# #             )

# #             print(
# #                 sorted(
# #                     true_positives
# #                 )
# #             )

# #             print()

# #             print(
# #                 "Missing Skills:"
# #             )

# #             print(
# #                 sorted(
# #                     false_negatives
# #                 )
# #             )

# #             print()

# #             print(
# #                 "Extra Skills:"
# #             )

# #             print(
# #                 sorted(
# #                     false_positives
# #                 )
# #             )


# #         except Exception as e:

# #             print()

# #             print(
# #                 f"ERROR processing "
# #                 f"{file.name}"
# #             )

# #             print(
# #                 repr(e)
# #             )

# #             continue


# #     # ========================================================
# #     # OVERALL EVALUATION
# #     # ========================================================

# #     print()
# #     print()
# #     print("=" * 70)
# #     print("OVERALL EVALUATION")
# #     print("=" * 70)

# #     print()


# #     print(
# #         f"Resumes evaluated : "
# #         f"{evaluated_resumes}"
# #     )


# #     print(
# #         f"Resumes skipped   : "
# #         f"{skipped_resumes}"
# #     )


# #     precision_denominator = (
# #         total_true_positives
# #         + total_false_positives
# #     )


# #     recall_denominator = (
# #         total_true_positives
# #         + total_false_negatives
# #     )


# #     overall_precision = (
# #         total_true_positives
# #         / precision_denominator
# #         if precision_denominator > 0
# #         else 0
# #     )


# #     overall_recall = (
# #         total_true_positives
# #         / recall_denominator
# #         if recall_denominator > 0
# #         else 0
# #     )


# #     overall_f1 = (
# #         2
# #         * overall_precision
# #         * overall_recall
# #         / (
# #             overall_precision
# #             + overall_recall
# #         )
# #         if (
# #             overall_precision
# #             + overall_recall
# #         ) > 0
# #         else 0
# #     )


# #     print()


# #     print(
# #         f"Total True Positives  : "
# #         f"{total_true_positives}"
# #     )


# #     print(
# #         f"Total False Positives : "
# #         f"{total_false_positives}"
# #     )


# #     print(
# #         f"Total False Negatives : "
# #         f"{total_false_negatives}"
# #     )


# #     print()


# #     print(
# #         f"Overall Precision     : "
# #         f"{overall_precision:.2f}"
# #     )


# #     print(
# #         f"Overall Recall        : "
# #         f"{overall_recall:.2f}"
# #     )


# #     print(
# #         f"Overall F1 Score      : "
# #         f"{overall_f1:.2f}"
# #     )


# #     print()
# #     print("=" * 70)


# # # ============================================================
# # # ENTRY POINT
# # # ============================================================

# # if __name__ == "__main__":
# #     main()
    

# """Code with Gemini API"""
# import os
# import time
# from pathlib import Path

# import pdfplumber
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# from app.db.save_candidate import save_resume_to_db
# from app.models.resume import Resume
# from app.utils.ground_truth import GROUND_TRUTH_DATA
# from app.utils.section_extractor import (
#     extract_experience_section,
#     extract_education_section,
#     extract_name_section,
# )


# # ============================================================
# # CONFIGURATION
# # ============================================================

# MODEL_NAME = "gemini-2.5-flash"

# FOLDER_PATH = Path(
#     "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/"
#     "Medline/Sr.Mgr FP&A/test"
# )

# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# ENV_PATH = PROJECT_ROOT / ".env"

# load_dotenv(ENV_PATH)

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError(
#         f"GEMINI_API_KEY not found in {ENV_PATH}"
#     )

# client = genai.Client(
#     api_key=api_key
# )


# print("=" * 70)
# print("PROVIDER CONFIGURATION")
# print("=" * 70)
# print("Provider : Gemini")
# print(f"Model    : {MODEL_NAME}")
# print(f"API key  : {'YES' if api_key else 'NO'}")
# print(f".env     : {ENV_PATH}")
# print("=" * 70)


# # ============================================================
# # NORMALIZATION
# # ============================================================

# def normalize_name(name: str) -> str:

#     if not name:
#         return ""

#     return " ".join(
#         name.upper().split()
#     )


# def normalize_skill(skill: str) -> str:

#     if not skill:
#         return ""

#     return " ".join(
#         skill.upper().split()
#     )


# NORMALIZED_GROUND_TRUTH = {
#     normalize_name(name): skills
#     for name, skills in GROUND_TRUTH_DATA.items()
# }


# def get_ground_truth_skills(name: str):

#     normalized_name = normalize_name(name)

#     if not normalized_name:
#         return None

#     return NORMALIZED_GROUND_TRUTH.get(
#         normalized_name
#     )


# # ============================================================
# # PDF EXTRACTION
# # ============================================================

# def extract_text(file_path: Path) -> str:

#     start = time.time()

#     if not file_path.exists():
#         raise FileNotFoundError(
#             f"PDF not found: {file_path}"
#         )

#     extracted_text = []

#     with pdfplumber.open(file_path) as pdf:

#         for page in pdf.pages:

#             page_text = page.extract_text()

#             if page_text:
#                 extracted_text.append(
#                     page_text
#                 )

#     elapsed = time.time() - start

#     print(
#         f"PDF extraction time: "
#         f"{elapsed:.2f} seconds"
#     )

#     return "\n\n".join(
#         extracted_text
#     )


# # ============================================================
# # GEMINI EXTRACTION
# # ============================================================

# def parse_resume_to_pydantic(
#     candidate_name: str,
#     experience_text: str,
#     education_text: str,
# ) -> Resume:

#     start = time.time()

#     prompt = f"""
# You are extracting structured information from a resume.

# CURRENT DATE:
# August 2026

# CANDIDATE NAME:
# {candidate_name}

# EXPERIENCE:
# {experience_text}

# EDUCATION:
# {education_text}

# Rules:

# - Use only information supported by the supplied resume text.
# - Use the supplied candidate name exactly.
# - Extract every professional employment record.
# - For each job extract company, title, start_date, end_date.
# - Normalize dates where possible.
# - Treat Current, Present, Till Date and To Date as August 2026.
# - Calculate total professional experience from the employment periods.
# - Do not double-count overlapping employment.
# - Do not estimate experience from seniority or title.
# - Extract professional skills from EXPERIENCE only.
# - Include technologies, tools, finance/accounting skills,
#   business domains, methodologies and clearly demonstrated processes.
# - Do not include company names, job titles, degrees or unsupported skills.
# - Extract education only from the supplied education text.
# """

#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             temperature=0,
#             response_mime_type="application/json",
#             response_schema=Resume,
#         ),
#     )

#     result = Resume.model_validate_json(
#         response.text
#     )

#     elapsed = time.time() - start

#     print(
#         f"Gemini extraction time: "
#         f"{elapsed:.2f} seconds"
#     )

#     return result


# # ============================================================
# # EVALUATION
# # ============================================================

# def precision_test(
#     ground_truth,
#     extracted_skills,
# ):

#     ground_truth_set = {
#         normalize_skill(skill)
#         for skill in ground_truth
#         if skill
#     }

#     extracted_skills_set = {
#         normalize_skill(skill)
#         for skill in extracted_skills
#         if skill
#     }

#     true_positives = (
#         ground_truth_set
#         & extracted_skills_set
#     )

#     false_positives = (
#         extracted_skills_set
#         - ground_truth_set
#     )

#     false_negatives = (
#         ground_truth_set
#         - extracted_skills_set
#     )

#     precision_denominator = (
#         len(true_positives)
#         + len(false_positives)
#     )

#     recall_denominator = (
#         len(true_positives)
#         + len(false_negatives)
#     )

#     precision = (
#         len(true_positives)
#         / precision_denominator
#         if precision_denominator > 0
#         else 0
#     )

#     recall = (
#         len(true_positives)
#         / recall_denominator
#         if recall_denominator > 0
#         else 0
#     )

#     f1_score = (
#         2 * precision * recall
#         / (precision + recall)
#         if precision + recall > 0
#         else 0
#     )

#     return (
#         precision,
#         recall,
#         f1_score,
#         true_positives,
#         false_positives,
#         false_negatives,
#     )


# # ============================================================
# # MAIN
# # ============================================================

# def main():

#     pdf_files = list(
#         FOLDER_PATH.glob("*.pdf")
#     )

#     print()
#     print(
#         f"Found {len(pdf_files)} PDF files."
#     )

#     total_true_positives = 0
#     total_false_positives = 0
#     total_false_negatives = 0

#     evaluated_resumes = 0
#     skipped_resumes = 0


#     for file in pdf_files:

#         print()
#         print("=" * 70)
#         print(f"Processing: {file.name}")
#         print("=" * 70)

#         try:

#             # ----------------------------------------------
#             # STEP 1 — PDF
#             # ----------------------------------------------

#             full_text = extract_text(
#                 file
#             )

#             print(
#                 f"Extracted characters: "
#                 f"{len(full_text)}"
#             )


#             # ----------------------------------------------
#             # STEP 2 — NAME
#             # ----------------------------------------------

#             name = extract_name_section(
#                 full_text
#             )

#             print(
#                 f"Candidate: {name}"
#             )


#             # ----------------------------------------------
#             # STEP 3 — EXPERIENCE
#             # ----------------------------------------------

#             experience_section = (
#                 extract_experience_section(
#                     full_text
#                 )
#             )

#             print(
#                 f"Experience characters: "
#                 f"{len(experience_section)}"
#             )


#             # ----------------------------------------------
#             # STEP 4 — EDUCATION
#             # ----------------------------------------------

#             education_section = (
#                 extract_education_section(
#                     full_text
#                 )
#             )

#             print(
#                 f"Education characters: "
#                 f"{len(education_section)}"
#             )


#             # ----------------------------------------------
#             # STEP 5 — GEMINI → PYDANTIC
#             # ----------------------------------------------

#             print()
#             print(
#                 "Sending resume sections "
#                 "to Gemini..."
#             )

#             llm_results = (
#                 parse_resume_to_pydantic(
#                     candidate_name=name,
#                     experience_text=experience_section,
#                     education_text=education_section,
#                 )
#             )

#             # Deterministic name wins
#             llm_results.name = name


#             # ----------------------------------------------
#             # STEP 6 — SAVE + LOCAL EMBEDDING
#             # ----------------------------------------------

#             print()
#             print(
#                 "Saving candidate to PostgreSQL..."
#             )

#             saved_candidate = (
#                 save_resume_to_db(
#                     resume=llm_results,
#                     resume_text=full_text,
#                 )
#             )


#             # ----------------------------------------------
#             # STEP 7 — OUTPUT
#             # ----------------------------------------------

#             print()
#             print("-" * 70)
#             print("EXTRACTED RESUME")
#             print("-" * 70)

#             print(
#                 f"Candidate: "
#                 f"{llm_results.name}"
#             )

#             print(
#                 f"Experience Years: "
#                 f"{llm_results.experience_years}"
#             )

#             print(
#                 f"Skills: "
#                 f"{llm_results.skills}"
#             )

#             print(
#                 f"Experience: "
#                 f"{llm_results.experience}"
#             )

#             print(
#                 f"Education: "
#                 f"{llm_results.education}"
#             )

#             print()
#             print("-" * 70)
#             print("DATABASE")
#             print("-" * 70)

#             print(
#                 f"Database ID: "
#                 f"{saved_candidate.id}"
#             )

#             print(
#                 f"Saved candidate: "
#                 f"{saved_candidate.name}"
#             )


#             # ----------------------------------------------
#             # STEP 8 — OPTIONAL EVALUATION
#             # ----------------------------------------------

#             ground_truth_skills = (
#                 get_ground_truth_skills(
#                     name
#                 )
#             )

#             if ground_truth_skills is None:

#                 skipped_resumes += 1
#                 continue


#             (
#                 precision,
#                 recall,
#                 f1_score,
#                 true_positives,
#                 false_positives,
#                 false_negatives,
#             ) = precision_test(
#                 ground_truth_skills,
#                 llm_results.skills,
#             )


#             total_true_positives += (
#                 len(true_positives)
#             )

#             total_false_positives += (
#                 len(false_positives)
#             )

#             total_false_negatives += (
#                 len(false_negatives)
#             )

#             evaluated_resumes += 1


#             print()
#             print("=" * 70)
#             print("RESULT")
#             print("=" * 70)

#             print(
#                 f"Precision: "
#                 f"{precision:.2f}"
#             )

#             print(
#                 f"Recall: "
#                 f"{recall:.2f}"
#             )

#             print(
#                 f"F1 Score: "
#                 f"{f1_score:.2f}"
#             )


#         except Exception as e:

#             print()
#             print(
#                 f"ERROR processing "
#                 f"{file.name}"
#             )

#             print(
#                 repr(e)
#             )


#     # ========================================================
#     # OVERALL
#     # ========================================================

#     print()
#     print("=" * 70)
#     print("OVERALL EVALUATION")
#     print("=" * 70)

#     precision_denominator = (
#         total_true_positives
#         + total_false_positives
#     )

#     recall_denominator = (
#         total_true_positives
#         + total_false_negatives
#     )

#     overall_precision = (
#         total_true_positives
#         / precision_denominator
#         if precision_denominator
#         else 0
#     )

#     overall_recall = (
#         total_true_positives
#         / recall_denominator
#         if recall_denominator
#         else 0
#     )

#     overall_f1 = (
#         2
#         * overall_precision
#         * overall_recall
#         / (
#             overall_precision
#             + overall_recall
#         )
#         if (
#             overall_precision
#             + overall_recall
#         )
#         else 0
#     )

#     print(
#         f"Resumes evaluated: "
#         f"{evaluated_resumes}"
#     )

#     print(
#         f"Resumes skipped: "
#         f"{skipped_resumes}"
#     )

#     print(
#         f"Overall Precision: "
#         f"{overall_precision:.2f}"
#     )

#     print(
#         f"Overall Recall: "
#         f"{overall_recall:.2f}"
#     )

#     print(
#         f"Overall F1: "
#         f"{overall_f1:.2f}"
#     )


# if __name__ == "__main__":
#     main()

# app/services/resume_extractor.py

import json
import os
import re
import time
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError, APIConnectionError

from app.models.resume import Resume
from app.utils.section_extractor import (
    extract_experience_section,
    extract_education_section,
    extract_name_section,
)


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

if not NVIDIA_API_KEY:
    raise ValueError(
        f"NVIDIA_API_KEY not found in {ENV_PATH}"
    )


client = OpenAI(
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    timeout=90.0,
    max_retries=0,
)


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_text(pdf_path: Path) -> str:
    """
    Reads all text from one PDF.
    """

    start = time.perf_counter()

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    extracted_text = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text.append(page_text)

    full_text = "\n\n".join(extracted_text)

    elapsed = time.perf_counter() - start

    print(
        f"[TIMING] PDF extraction: "
        f"{elapsed:.2f}s"
    )

    print(
        f"[INFO] Full text characters: "
        f"{len(full_text)}"
    )

    return full_text


# ============================================================
# EXPERIENCE YEARS NORMALIZATION
# ============================================================

def parse_experience_years(value) -> float:
    """
    Converts values such as:
    '14 years'
    '14 years 6 months'
    '14.5'
    into a float.
    """

    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).lower()

    years = 0.0
    months = 0.0

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*years?",
        text,
    )

    month_match = re.search(
        r"(\d+)\s*months?",
        text,
    )

    if year_match:
        years = float(
            year_match.group(1)
        )

    if month_match:
        months = float(
            month_match.group(1)
        )

    if years == 0 and months == 0:

        number_match = re.search(
            r"\d+(?:\.\d+)?",
            text,
        )

        if number_match:
            return float(
                number_match.group()
            )

        return 0.0

    return years + (months / 12)


# ============================================================
# NORMALIZE NVIDIA OUTPUT
# ============================================================

def normalize_resume_payload(
    payload: dict,
) -> dict:
    """
    Repairs common response shape differences
    before Pydantic validation.
    """

    # EXPERIENCE
    experience = payload.get("experience")

    if isinstance(experience, dict):

        records = experience.get(
            "records",
            [],
        )

        payload["experience"] = records

        if not payload.get(
            "experience_years"
        ):

            total_experience = (
                experience.get(
                    "total_experience"
                )
            )

            if total_experience:
                payload["experience_years"] = (
                    parse_experience_years(
                        total_experience
                    )
                )

    # EXPERIENCE YEARS
    payload["experience_years"] = (
        parse_experience_years(
            payload.get(
                "experience_years"
            )
        )
    )

    # EDUCATION
    education = payload.get("education")

    if isinstance(education, dict):

        payload["education"] = (
            education.get(
                "records",
                [],
            )
        )

    # SKILLS
    skills = payload.get("skills")

    if skills is None:

        payload["skills"] = []

    elif isinstance(skills, str):

        payload["skills"] = [
            skill.strip()
            for skill in skills.split(",")
            if skill.strip()
        ]

    # GUARANTEE LIST FIELDS
    if payload.get("experience") is None:
        payload["experience"] = []

    if payload.get("education") is None:
        payload["education"] = []

    if payload.get("skills") is None:
        payload["skills"] = []

    if payload.get("projects") is None:
        payload["projects"] = []

    return payload


# ============================================================
# NVIDIA CALL
# ============================================================

def call_nvidia_model(
    prompt: str,
) -> str:
    """
    Sends the prompt to NVIDIA and prints timing.
    """

    print(
        "\n>>> About to call NVIDIA API"
    )

    print(
        f">>> Prompt size: "
        f"{len(prompt)} characters"
    )

    start = time.perf_counter()

    try:

        response = (
            client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a resume "
                            "information extraction "
                            "system. Return only "
                            "valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
            )
        )

    except APITimeoutError as error:

        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            f">>> NVIDIA TIMEOUT "
            f"after {elapsed:.2f}s"
        )

        raise RuntimeError(
            "NVIDIA request timed out."
        ) from error

    except APIConnectionError as error:

        print(
            ">>> Could not connect "
            "to NVIDIA API"
        )

        raise RuntimeError(
            "NVIDIA API connection failed."
        ) from error

    except Exception as error:

        print(
            f">>> NVIDIA ERROR: "
            f"{type(error).__name__}: "
            f"{error}"
        )

        raise

    elapsed = (
        time.perf_counter()
        - start
    )

    print(
        f">>> NVIDIA responded in "
        f"{elapsed:.2f}s"
    )

    if response.usage:

        print(
            f">>> Prompt tokens: "
            f"{response.usage.prompt_tokens}"
        )

        print(
            f">>> Completion tokens: "
            f"{response.usage.completion_tokens}"
        )

        print(
            f">>> Total tokens: "
            f"{response.usage.total_tokens}"
        )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    if not content:
        raise ValueError(
            "NVIDIA returned an empty response."
        )

    return content


# ============================================================
# CLEAN OPTIONAL JSON CODE FENCES
# ============================================================

def clean_json_response(
    response_text: str,
) -> str:
    """
    Removes ```json and ``` if the model
    wraps JSON in markdown.
    """

    text = response_text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ============================================================
# STRUCTURED RESUME EXTRACTION
# ============================================================

def parse_resume_to_pydantic(
    candidate_name: str,
    experience_text: str,
    education_text: str,
) -> Resume:
    """
    Sends only relevant resume sections
    to NVIDIA and returns a Resume model.
    """

    start = time.perf_counter()

    prompt = f"""
Extract structured information from this resume.

CURRENT DATE:
August 2026

CANDIDATE NAME:
{candidate_name}

EXPERIENCE SECTION:
{experience_text}

EDUCATION SECTION:
{education_text}


Return ONLY valid JSON with this structure:

{{
    "name": "{candidate_name}",
    "experience_years": 0.0,
    "skills": [],
    "experience": [],
    "education": [],
    "projects": []
}}


RULES:

NAME
- Use the supplied candidate name exactly.

EXPERIENCE
- Extract every clearly identifiable professional employment record.
- Each record must contain:
  company,
  title,
  start_date,
  end_date.
- Do not invent missing information.

EXPERIENCE YEARS
- Must be numeric.
- Calculate from employment dates.
- Treat Present, Current, Till Date and To Date
  as August 2026.
- Do not double-count overlapping employment.
- Do not estimate from seniority, title,
  age or number of jobs.

SKILLS
- Extract professional skills demonstrated
  in EXPERIENCE.
- Include technologies, tools, software,
  platforms, finance skills,
  accounting skills, business domains,
  analytical skills, methodologies
  and professional processes.

Do NOT include:
- candidate names
- company names
- job titles
- degrees
- unsupported capabilities

EDUCATION
- Extract only from the EDUCATION section.
- Each record should contain:
  degree,
  institution,
  start_date,
  end_date.
- Use empty strings when a value is unavailable.
- Do not invent information.

PROJECTS
- Return an empty list unless projects are
  clearly available in the supplied text.
"""

    response_text = call_nvidia_model(
        prompt
    )

    response_text = clean_json_response(
        response_text
    )

    try:

        payload = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:

        print(
            "\n[ERROR] NVIDIA raw response:"
        )

        print(response_text)

        raise ValueError(
            "NVIDIA returned invalid JSON."
        ) from error

    payload = normalize_resume_payload(
        payload
    )

    # Deterministic name extractor wins
    payload["name"] = candidate_name

    resume = Resume.model_validate(
        payload
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    print(
        f"[TIMING] Complete LLM parsing: "
        f"{elapsed:.2f}s"
    )

    return resume


# ============================================================
# COMPLETE RESUME PIPELINE
# ============================================================

def extract_resume_data(
    pdf_path: Path,
) -> Resume:
    """
    Complete pipeline:
    PDF
      -> raw text
      -> name
      -> experience section
      -> education section
      -> NVIDIA
      -> Pydantic Resume
    """

    pipeline_start = (
        time.perf_counter()
    )

    print(
        "\n"
        + "=" * 60
    )

    print(
        f"Starting resume extraction: "
        f"{Path(pdf_path).name}"
    )

    print(
        "=" * 60
    )

    # STEP 1 — PDF
    full_text = extract_text(
        pdf_path
    )

    if not full_text.strip():
        raise ValueError(
            "No text could be extracted "
            "from the PDF."
        )

    # STEP 2 — NAME
    start = time.perf_counter()

    name = extract_name_section(
        full_text
    )

    print(
        f"[TIMING] Name extraction: "
        f"{time.perf_counter() - start:.4f}s"
    )

    print(
        f"[INFO] Candidate name: {name}"
    )

    # STEP 3 — EXPERIENCE
    start = time.perf_counter()

    experience_section = (
        extract_experience_section(
            full_text
        )
    )

    print(
        f"[TIMING] Experience section: "
        f"{time.perf_counter() - start:.4f}s"
    )

    print(
        f"[INFO] Experience characters: "
        f"{len(experience_section)}"
    )

    # STEP 4 — EDUCATION
    start = time.perf_counter()

    education_section = (
        extract_education_section(
            full_text
        )
    )

    print(
        f"[TIMING] Education section: "
        f"{time.perf_counter() - start:.4f}s"
    )

    print(
        f"[INFO] Education characters: "
        f"{len(education_section)}"
    )

    # CONTEXT SIZE
    relevant_chars = (
        len(experience_section)
        + len(education_section)
    )

    print(
        f"[INFO] Full resume characters: "
        f"{len(full_text)}"
    )

    print(
        f"[INFO] Relevant context characters: "
        f"{relevant_chars}"
    )

    if len(full_text) > 0:

        reduction = (
            1
            - relevant_chars
            / len(full_text)
        ) * 100

        print(
            f"[INFO] Context reduction: "
            f"{reduction:.1f}%"
        )

    # STEP 5 — NVIDIA
    print(
        "\n[STAGE] Starting NVIDIA extraction..."
    )

    resume = parse_resume_to_pydantic(
        candidate_name=name,
        experience_text=experience_section,
        education_text=education_section,
    )

    resume.name = name

    total_elapsed = (
        time.perf_counter()
        - pipeline_start
    )

    print(
        "\n"
        + "=" * 60
    )

    print(
        f"[TIMING] TOTAL PIPELINE: "
        f"{total_elapsed:.2f}s"
    )

    print(
        "=" * 60
    )

    return resume


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    pdf_path = Path(
        "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/Sent/Manalot_Anup_Dubey.pdf"
    )

    print(
        "Starting resume extraction..."
    )

    resume = extract_resume_data(
        pdf_path
    )

    print(
        "\nFinished."
    )

    print(
        resume.model_dump()
    )