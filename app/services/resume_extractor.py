import os
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        f"GEMINI_API_KEY not found in {ENV_PATH}"
    )

client = genai.Client(
    api_key=api_key
)

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text(
    pdf_path: Path,
) -> str:

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    extracted_text = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text.append(
                    page_text
                )

    return "\n\n".join(
        extracted_text
    )


# ============================================================
# GEMINI STRUCTURED EXTRACTION
# ============================================================

def parse_resume_to_pydantic(
    candidate_name: str,
    experience_text: str,
    education_text: str,
) -> Resume:

    prompt = f"""
You are extracting structured information from a resume.

CURRENT DATE:
August 2026

CANDIDATE NAME:
{candidate_name}

EXPERIENCE:
{experience_text}

EDUCATION:
{education_text}

Rules:

- Use only information supported by the supplied resume text.
- Use the supplied candidate name exactly.
- Extract every professional employment record.
- For each job extract company, title, start_date, end_date.
- Normalize dates where possible.
- Treat Current, Present, Till Date and To Date as August 2026.
- Calculate total professional experience from the employment periods.
- Do not double-count overlapping employment.
- Do not estimate experience from seniority or title.

SKILLS:

- Extract professional skills from EXPERIENCE only.
- Include technologies, tools, software, platforms,
  finance/accounting skills, business domains,
  methodologies, analytical skills and clearly
  demonstrated professional processes.
- Do not include company names.
- Do not include job titles.
- Do not include degrees.
- Do not invent unsupported skills.

EDUCATION:

- Extract education only from the supplied education text.
- Extract every clearly identifiable education record.
- Include degree, institution, start_date and end_date
  when available.
- Do not invent missing information.

Return data matching the Resume schema.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=Resume,
        ),
    )

    return Resume.model_validate_json(
        response.text
    )


# ============================================================
# COMPLETE RESUME PIPELINE
# ============================================================

def extract_resume_data(
    pdf_path: Path,
) -> Resume:

    # 1. PDF -> full text
    full_text = extract_text(
        pdf_path
    )

    if not full_text.strip():
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    # 2. Deterministic name extraction
    name = extract_name_section(
        full_text
    )

    # 3. Experience section
    experience_section = (
        extract_experience_section(
            full_text
        )
    )

    # 4. Education section
    education_section = (
        extract_education_section(
            full_text
        )
    )

    # 5. Gemini -> Resume Pydantic model
    resume = parse_resume_to_pydantic(
        candidate_name=name,
        experience_text=experience_section,
        education_text=education_section,
    )

    # Deterministic extractor wins for name
    resume.name = name

    return resume

"""nvidia API"""
# import json
# import os
# import re
# from pathlib import Path

# import pdfplumber
# from dotenv import load_dotenv
# from openai import OpenAI

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

# NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
# NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
# NVIDIA_MODEL ="nvidia/nemotron-3.5-lightning-30b-a3b"

# if not NVIDIA_API_KEY:
#     raise ValueError(
#         f"NVIDIA_API_KEY not found in {ENV_PATH}"
#     )

# if not NVIDIA_BASE_URL:
#     raise ValueError(
#         "NVIDIA_BASE_URL not configured."
#     )

# if not NVIDIA_MODEL:
#     raise ValueError(
#         "NVIDIA_MODEL not configured."
#     )


# client = OpenAI(
#     api_key=NVIDIA_API_KEY,
#     base_url=NVIDIA_BASE_URL,
# )


# # ============================================================
# # PDF EXTRACTION
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
# # EXPERIENCE YEAR NORMALIZATION
# # ============================================================

# def parse_experience_years(
#     value,
# ) -> float:

#     if value is None:
#         return 0.0

#     if isinstance(
#         value,
#         (int, float),
#     ):
#         return float(value)

#     text = str(value).lower()

#     years = 0.0
#     months = 0.0

#     year_match = re.search(
#         r"(\d+(?:\.\d+)?)\s*years?",
#         text,
#     )

#     month_match = re.search(
#         r"(\d+)\s*months?",
#         text,
#     )

#     if year_match:
#         years = float(
#             year_match.group(1)
#         )

#     if month_match:
#         months = float(
#             month_match.group(1)
#         )

#     if years == 0 and months == 0:

#         number_match = re.search(
#             r"\d+(?:\.\d+)?",
#             text,
#         )

#         if number_match:
#             return float(
#                 number_match.group()
#             )

#         return 0.0

#     return years + (
#         months / 12
#     )


# # ============================================================
# # PROVIDER NORMALIZATION
# # ============================================================

# def normalize_resume_payload(
#     payload: dict,
# ) -> dict:

#     # --------------------------------------------------------
#     # EXPERIENCE
#     # --------------------------------------------------------

#     experience = payload.get(
#         "experience"
#     )

#     if isinstance(
#         experience,
#         dict,
#     ):

#         # NVIDIA may return:
#         #
#         # {
#         #   "experience": {
#         #       "total_experience": "14 years",
#         #       "records": [...]
#         #   }
#         # }

#         records = experience.get(
#             "records",
#             []
#         )

#         payload["experience"] = (
#             records
#         )

#         if not payload.get(
#             "experience_years"
#         ):

#             total_experience = (
#                 experience.get(
#                     "total_experience"
#                 )
#             )

#             if total_experience:

#                 payload[
#                     "experience_years"
#                 ] = parse_experience_years(
#                     total_experience
#                 )


#     # --------------------------------------------------------
#     # EDUCATION
#     # --------------------------------------------------------

#     education = payload.get(
#         "education"
#     )

#     if isinstance(
#         education,
#         dict,
#     ):

#         payload["education"] = (
#             education.get(
#                 "records",
#                 []
#             )
#         )


#     # --------------------------------------------------------
#     # SKILLS
#     # --------------------------------------------------------

#     skills = payload.get(
#         "skills"
#     )

#     if skills is None:

#         payload["skills"] = []

#     elif isinstance(
#         skills,
#         str,
#     ):

#         payload["skills"] = [
#             skill.strip()
#             for skill in skills.split(",")
#             if skill.strip()
#         ]


#     # --------------------------------------------------------
#     # GUARANTEE LISTS
#     # --------------------------------------------------------

#     if payload.get("experience") is None:
#         payload["experience"] = []

#     if payload.get("education") is None:
#         payload["education"] = []

#     if payload.get("skills") is None:
#         payload["skills"] = []


#     return payload


# # ============================================================
# # NVIDIA CALL
# # ============================================================

# def call_nvidia_model(
#     prompt: str,
# ) -> str:

#     response = client.chat.completions.create(
#         model=NVIDIA_MODEL,

#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a resume information "
#                     "extraction system. Return only "
#                     "valid JSON."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": prompt,
#             },
#         ],

#         temperature=0,
#     )

#     content = (
#         response
#         .choices[0]
#         .message
#         .content
#     )

#     if not content:
#         raise ValueError(
#             "NVIDIA returned an empty response."
#         )

#     return content


# # ============================================================
# # REMOVE OPTIONAL MARKDOWN CODE FENCES
# # ============================================================

# def clean_json_response(
#     response_text: str,
# ) -> str:

#     text = response_text.strip()

#     if text.startswith("```json"):
#         text = text[7:]

#     elif text.startswith("```"):
#         text = text[3:]

#     if text.endswith("```"):
#         text = text[:-3]

#     return text.strip()


# # ============================================================
# # STRUCTURED RESUME EXTRACTION
# # ============================================================

# def parse_resume_to_pydantic(
#     candidate_name: str,
#     experience_text: str,
#     education_text: str,
# ) -> Resume:

#     prompt = f"""
# Extract structured information from this resume.

# CURRENT DATE:
# August 2026

# CANDIDATE NAME:
# {candidate_name}


# EXPERIENCE SECTION:

# {experience_text}


# EDUCATION SECTION:

# {education_text}


# Return ONLY valid JSON.

# Use exactly this top-level structure:

# {{
#     "name": "{candidate_name}",
#     "experience_years": 0.0,
#     "skills": [],
#     "experience": [],
#     "education": []
# }}


# IMPORTANT STRUCTURE RULES:


# 1. NAME

# "name" must be a string.

# Use this name exactly:

# {candidate_name}


# 2. EXPERIENCE YEARS

# "experience_years" must be a numeric value.

# Examples:

# 15 years
# -> 15.0

# 15 years 6 months
# -> 15.5

# 10 years 3 months
# -> 10.25

# Do NOT return:

# "experience_years": "15 years"


# 3. EXPERIENCE

# "experience" MUST be a JSON array.

# Correct:

# "experience": [
#     {{
#         "company": "ABC Ltd",
#         "title": "Finance Manager",
#         "start_date": "Jan 2020",
#         "end_date": "Dec 2024"
#     }}
# ]

# Incorrect:

# "experience": {{
#     "records": [...]
# }}

# Incorrect:

# "experience": {{
#     "total_experience": "...",
#     "records": [...]
# }}

# Do not place total experience inside the
# experience field.


# 4. EDUCATION

# "education" MUST be a JSON array.

# Correct:

# "education": [
#     {{
#         "degree": "MBA",
#         "institution": "XYZ University",
#         "start_date": "1996",
#         "end_date": "1998"
#     }}
# ]

# Incorrect:

# "education": {{
#     "records": [...]
# }}


# 5. SKILLS

# "skills" MUST be an array of strings.

# Correct:

# "skills": [
#     "FP&A",
#     "Forecasting",
#     "SAP",
#     "Power BI"
# ]

# Do not return a comma-separated string.


# CONTENT RULES:

# - Use only information supported by the supplied text.

# - Extract every clearly identifiable
#   professional employment record.

# - For every employment record extract:
#   company,
#   title,
#   start_date,
#   end_date.

# - Normalize dates where possible.

# - Treat Present, Current, Till Date and
#   To Date as August 2026 when calculating
#   experience.

# - Calculate total professional experience
#   from employment periods.

# - Do not double-count overlapping
#   employment periods.

# - Do not estimate experience from:
#   title,
#   seniority,
#   age,
#   or number of jobs.

# - Extract professional skills from
#   EXPERIENCE only.

# - Skills may include:
#   technologies,
#   tools,
#   software,
#   platforms,
#   finance skills,
#   accounting skills,
#   business domains,
#   analytical skills,
#   methodologies,
#   professional processes.

# - Do not include as skills:
#   candidate name,
#   company names,
#   job titles,
#   degrees,
#   unsupported capabilities.

# - Extract education only from the
#   EDUCATION section.

# - Do not invent missing information.
# """

#     response_text = call_nvidia_model(
#         prompt
#     )

#     response_text = clean_json_response(
#         response_text
#     )

#     try:

#         payload = json.loads(
#             response_text
#         )

#     except json.JSONDecodeError as e:

#         raise ValueError(
#             "NVIDIA returned invalid JSON."
#         ) from e


#     payload = normalize_resume_payload(
#         payload
#     )


#     # Deterministic name extractor wins
#     payload["name"] = candidate_name


#     return Resume.model_validate(
#         payload
#     )


# # ============================================================
# # COMPLETE RESUME PIPELINE
# # ============================================================

# def extract_resume_data(
#     pdf_path: Path,
# ) -> Resume:

#     # --------------------------------------------------------
#     # STEP 1 — PDF -> TEXT
#     # --------------------------------------------------------

#     full_text = extract_text(
#         pdf_path
#     )

#     if not full_text.strip():

#         raise ValueError(
#             "No text could be extracted "
#             "from the PDF."
#         )


#     # --------------------------------------------------------
#     # STEP 2 — NAME
#     # --------------------------------------------------------

#     name = extract_name_section(
#         full_text
#     )


#     # --------------------------------------------------------
#     # STEP 3 — EXPERIENCE
#     # --------------------------------------------------------

#     experience_section = (
#         extract_experience_section(
#             full_text
#         )
#     )


#     # --------------------------------------------------------
#     # STEP 4 — EDUCATION
#     # --------------------------------------------------------

#     education_section = (
#         extract_education_section(
#             full_text
#         )
#     )


#     # --------------------------------------------------------
#     # STEP 5 — NVIDIA -> RESUME MODEL
#     # --------------------------------------------------------

#     resume = parse_resume_to_pydantic(
#         candidate_name=name,
#         experience_text=experience_section,
#         education_text=education_section,
#     )


#     # Deterministic extractor wins
#     resume.name = name


#     return resume

if __name__ == "__main__":
    from pathlib import Path

    pdf_path = Path(
        "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/Sent/Manalot_Anup_Dubey.pdf"
    )

    print("Starting resume extraction...")

    resume = extract_resume_data(pdf_path)

    print("Finished.")
    print(resume.model_dump())