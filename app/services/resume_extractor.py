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
import os
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI

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

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError(
        f"NVIDIA_API_KEY not found in {ENV_PATH}"
    )

# Initialize NVIDIA NIM client with OpenAI-compatible interface
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)

# Using a high-quality NVIDIA model
MODEL_NAME = "nvidia/nemotron-3.5-lightning-30b-a3b"  # or "meta/llama-3.1-70b-instruct" etc.


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
# NVIDIA NIM STRUCTURED EXTRACTION
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

IMPORTANT: Return your response as a valid JSON object.
"""

    # NVIDIA NIM API call using OpenAI-compatible interface
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts structured information from resumes. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=4096,  # Adjust based on model context window
        response_format={"type": "json_object"}  # Request JSON output
    )

    # Extract the JSON response
    response_text = response.choices[0].message.content

    return Resume.model_validate_json(
        response_text
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

    # 5. NVIDIA NIM -> Resume Pydantic model
    resume = parse_resume_to_pydantic(
        candidate_name=name,
        experience_text=experience_section,
        education_text=education_section,
    )

    # Deterministic extractor wins for name
    resume.name = name

    return resume