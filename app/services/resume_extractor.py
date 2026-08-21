# import os
# from pathlib import Path

# import pdfplumber
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# from app.models.resume import Resume

# from app.utils.section_extractor import (
#     extract_experience_section,
#     extract_education_section,
#     extract_name_section,
# )


# # ============================================================
# # CONFIGURATION
# # ============================================================

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

# MODEL_NAME = "gemini-2.5-flash"


# # ============================================================
# # PDF TEXT EXTRACTION
# # ============================================================

# def extract_text(
#     pdf_path: Path,
# ) -> str:

#     if not pdf_path.exists():
#         raise FileNotFoundError(
#             f"PDF not found: {pdf_path}"
#         )

#     extracted_text = []

#     with pdfplumber.open(pdf_path) as pdf:

#         for page in pdf.pages:

#             page_text = page.extract_text()

#             if page_text:
#                 extracted_text.append(
#                     page_text
#                 )

#     return "\n\n".join(
#         extracted_text
#     )


# # ============================================================
# # GEMINI STRUCTURED EXTRACTION
# # ============================================================

# def parse_resume_to_pydantic(
#     candidate_name: str,
#     experience_text: str,
#     education_text: str,
# ) -> Resume:

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

# SKILLS:

# - Extract professional skills from EXPERIENCE only.
# - Include technologies, tools, software, platforms,
#   finance/accounting skills, business domains,
#   methodologies, analytical skills and clearly
#   demonstrated professional processes.
# - Do not include company names.
# - Do not include job titles.
# - Do not include degrees.
# - Do not invent unsupported skills.

# EDUCATION:

# - Extract education only from the supplied education text.
# - Extract every clearly identifiable education record.
# - Include degree, institution, start_date and end_date
#   when available.
# - Do not invent missing information.

# Return data matching the Resume schema.
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

#     return Resume.model_validate_json(
#         response.text
#     )


# # ============================================================
# # COMPLETE RESUME PIPELINE
# # ============================================================

# def extract_resume_data(
#     pdf_path: Path,
# ) -> Resume:

#     # 1. PDF -> full text
#     full_text = extract_text(
#         pdf_path
#     )

#     if not full_text.strip():
#         raise ValueError(
#             "No text could be extracted from the PDF."
#         )

#     # 2. Deterministic name extraction
#     name = extract_name_section(
#         full_text
#     )

#     # 3. Experience section
#     experience_section = (
#         extract_experience_section(
#             full_text
#         )
#     )

#     # 4. Education section
#     education_section = (
#         extract_education_section(
#             full_text
#         )
#     )

#     # 5. Gemini -> Resume Pydantic model
#     resume = parse_resume_to_pydantic(
#         candidate_name=name,
#         experience_text=experience_section,
#         education_text=education_section,
#     )

#     # Deterministic extractor wins for name
#     resume.name = name

#     return resume

"""nvidia API"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from app.models.resume import Resume


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


# ============================================================
# NORMALIZE PROVIDER OUTPUT
# ============================================================

def normalize_resume_payload(
    payload: dict,
) -> dict:

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    experience = payload.get(
        "experience"
    )

    if isinstance(
        experience,
        dict,
    ):

        # NVIDIA may return:
        #
        # "experience": {
        #     "total_experience": "...",
        #     "records": [...]
        # }

        records = experience.get(
            "records",
            []
        )

        payload["experience"] = records

        # If provider supplied total experience inside
        # experience, use it only if top-level
        # experience_years is missing.
        if (
            not payload.get("experience_years")
            and experience.get("total_experience")
        ):

            total_experience = (
                experience.get(
                    "total_experience"
                )
            )

            # Leave parsing to a helper below
            payload["experience_years"] = (
                parse_experience_years(
                    total_experience
                )
            )


    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    education = payload.get(
        "education"
    )

    if isinstance(
        education,
        dict,
    ):

        # NVIDIA may return:
        #
        # "education": {
        #     "records": [...]
        # }

        payload["education"] = (
            education.get(
                "records",
                []
            )
        )


    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    skills = payload.get(
        "skills"
    )

    if skills is None:
        payload["skills"] = []

    elif isinstance(
        skills,
        str,
    ):

        payload["skills"] = [
            skill.strip()
            for skill in skills.split(",")
            if skill.strip()
        ]


    # --------------------------------------------------------
    # GUARANTEE LIST FIELDS
    # --------------------------------------------------------

    if payload.get("experience") is None:
        payload["experience"] = []

    if payload.get("education") is None:
        payload["education"] = []


    return payload


# ============================================================
# EXPERIENCE YEAR PARSER
# ============================================================

def parse_experience_years(
    value,
) -> float:

    if value is None:
        return 0.0

    if isinstance(
        value,
        (int, float),
    ):
        return float(value)

    text = str(value).lower()

    years = 0.0
    months = 0.0

    import re

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

    if (
        years == 0
        and months == 0
    ):

        number_match = re.search(
            r"\d+(?:\.\d+)?",
            text,
        )

        if number_match:
            return float(
                number_match.group()
            )

        return 0.0

    return years + (
        months / 12
    )


# ============================================================
# NVIDIA RESUME EXTRACTION
# ============================================================

def parse_resume_to_pydantic(
    candidate_name: str,
    experience_text: str,
    education_text: str,
) -> Resume:

    prompt = f"""
You are extracting structured information from a resume.

CANDIDATE NAME:
{candidate_name}

EXPERIENCE SECTION:
{experience_text}

EDUCATION SECTION:
{education_text}


Return ONLY valid JSON.

The JSON MUST have exactly this top-level structure:

{{
    "name": "candidate name",
    "experience_years": 0.0,
    "skills": [],
    "experience": [],
    "education": []
}}


IMPORTANT OUTPUT RULES:

1. "experience_years"
   - Must be a number.
   - Example:
     14.5
   - Do NOT return:
     "14 years 6 months"

2. "experience"
   - Must be a JSON array.
   - Every item represents one employment record.

Example:

"experience": [
    {{
        "company": "ABC Ltd",
        "title": "Finance Manager",
        "start_date": "Jan 2020",
        "end_date": "Dec 2024"
    }}
]

Do NOT return:

"experience": {{
    "records": [...]
}}

Do NOT put "total_experience" inside "experience".


3. "education"
   - Must be a JSON array.

Example:

"education": [
    {{
        "degree": "MBA",
        "institution": "XYZ University",
        "start_date": "1996",
        "end_date": "1998"
    }}
]

Do NOT return:

"education": {{
    "records": [...]
}}


4. "skills"
   - Must be a JSON array of strings.

Example:

"skills": [
    "FP&A",
    "Forecasting",
    "SAP",
    "Power BI"
]


CONTENT RULES:

- Use only information supported by the resume.
- Use the supplied candidate name exactly.
- Extract every professional employment record.
- Extract company, title, start_date and end_date.
- Do not invent dates.
- Calculate total professional experience from employment periods.
- Do not double-count overlapping employment.
- Do not estimate experience from seniority or title.
- Extract professional skills from the EXPERIENCE section only.
- Do not include company names, job titles or degrees as skills.
- Extract education only from the EDUCATION section.
"""

    # --------------------------------------------------------
    # CALL NVIDIA HERE
    # --------------------------------------------------------
    #
    # Replace this block with whatever NVIDIA SDK/client
    # call you are already using.
    #
    # The important requirement is that response_text
    # becomes the raw JSON string returned by NVIDIA.
    # --------------------------------------------------------

    response_text = call_nvidia_model(
        prompt
    )


    # ========================================================
    # JSON PARSE
    # ========================================================

    try:

        payload = json.loads(
            response_text
        )

    except json.JSONDecodeError as e:

        raise ValueError(
            "NVIDIA returned invalid JSON."
        ) from e


    # ========================================================
    # NORMALIZE PROVIDER-SPECIFIC OUTPUT
    # ========================================================

    payload = normalize_resume_payload(
        payload
    )


    # Deterministic name wins
    payload["name"] = candidate_name


    # ========================================================
    # PYDANTIC VALIDATION
    # ========================================================

    return Resume.model_validate(
        payload
    )