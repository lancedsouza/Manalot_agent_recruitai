import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.candidate_profile import CandidateProfile
from app.models.role_benchmark import RoleBenchmark
from app.services.benchmark_validator import validate_benchmark


# ============================================================
# GEMINI CONFIG
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
# DYNAMIC BENCHMARK GENERATOR
# ============================================================

def generate_benchmark(
    candidate_profile: CandidateProfile,
) -> RoleBenchmark:

    prompt = f"""
You are creating a professional candidate evaluation benchmark.

Create an appropriate benchmark using this context:

FUNCTION:
{candidate_profile.function}

DESIGNATION:
{candidate_profile.designation}

EXPERIENCE:
{candidate_profile.experience_years} years

INDUSTRY:
{candidate_profile.industry}

GEOGRAPHY:
{candidate_profile.geography}

Your task is to determine WHAT should be evaluated for a professional
with this function and context.

Requirements:

1. Create between 5 and 8 meaningful evaluation dimensions.

2. Dimensions must be relevant to the candidate's function,
   seniority, experience, industry and geography.

3. Each dimension must have:
   - a clear name
   - a clear description
   - a weight

4. All weights must add up to exactly 1.0.

5. Avoid overlapping dimensions.

6. Do NOT evaluate or score this specific candidate.

7. Do NOT use achievements such as the candidate's team size,
   portfolio, business impact or skills to make the benchmark
   easier or harder for this particular candidate.

8. The benchmark should represent what a strong professional
   in this context should be evaluated on.
9.For each benchmark dimension:

- create 3 to 6 evaluation criteria
- each criterion must represent a distinct aspect of the dimension
- avoid duplicate or overlapping criteria
- criteria should be specific enough that a candidate can be assessed against them
- do not include candidate-specific achievements
- criteria must reflect the role context:
  function, designation, experience, industry, geography

Return the benchmark using the required schema.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=RoleBenchmark,
        ),
    )

    benchmark = RoleBenchmark.model_validate_json(
        response.text
    )

    validate_benchmark(
        benchmark
    )

    return benchmark