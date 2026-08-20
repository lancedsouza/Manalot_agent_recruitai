import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.candidate_profile import CandidateProfile
from app.models.role_benchmark import RoleBenchmark
from app.models.benchmark_score import BenchmarkEvaluation


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


def eval_candidate(
    candidate_profile: CandidateProfile,
    function_benchmark: RoleBenchmark,
) -> BenchmarkEvaluation:

    prompt = f"""
You are evaluating a candidate against a predefined
professional benchmark.

CANDIDATE PROFILE:

{candidate_profile.model_dump_json(indent=2)}

BENCHMARK:

{function_benchmark.model_dump_json(indent=2)}

INSTRUCTIONS:

Evaluate the candidate on EVERY benchmark dimension.

For each dimension:

1. Give a score from 0 to 10.
2. Use only evidence available in the candidate profile.
3. List the evidence supporting the score.
4. Explain briefly why the evidence justifies the score.
5. Do not invent missing achievements or responsibilities.
6. Missing information means "not evidenced", not necessarily poor ability.
IMPORTANT EVIDENCE RULES:

- Designation and years of experience are context only.
- Do NOT use designation alone as evidence of leadership,
  strategic responsibility, stakeholder altitude, scope,
  or business impact.

- Do NOT assume that because someone is a Director,
  VP, Manager, or other senior title that they necessarily
  demonstrated the expected capability.

- Prefer explicit evidence such as:
  team size,
  revenue owned,
  portfolio size,
  budget ownership,
  target attainment,
  markets handled,
  deal complexity,
  stakeholder level,
  measurable business outcomes,
  transformation ownership.

- Skills listed without supporting experience are weaker
  evidence than demonstrated achievements.

- If something is implied but not explicitly supported,
  state "not clearly evidenced" and score accordingly.

- Do not invent evidence.

IMPORTANT:

- Do not add new benchmark dimensions.
- Do not remove benchmark dimensions.
- Use the benchmark dimensions exactly as supplied.
- Consider designation, experience, industry and geography
  when interpreting the strength of the evidence.
- Return an overall analysis, strengths, weaknesses and
  practical improvements.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=BenchmarkEvaluation,
        ),
    )

    return BenchmarkEvaluation.model_validate_json(
        response.text
    )