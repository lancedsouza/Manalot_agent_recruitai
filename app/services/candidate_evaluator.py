import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.candidate_profile import CandidateProfile
from app.models.role_benchmark import RoleBenchmark
from app.models.benchmark_score import BenchmarkEvaluation


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
# VALIDATION
# ============================================================

def validate_evaluation(
    evaluation: BenchmarkEvaluation,
    benchmark: RoleBenchmark,
) -> None:

    # Every benchmark dimension should have a score
    if len(evaluation.dimension_scores) != len(
        benchmark.dimensions
    ):
        raise ValueError(
            "Evaluation does not contain a score "
            "for every benchmark dimension."
        )

    # Strengths should not be empty
    if len(evaluation.strengths) < 2:
        raise ValueError(
            "Evaluation must contain at least "
            "2 evidence-based strengths."
        )

    # Weaknesses / evidence gaps should not be empty
    if len(evaluation.weaknesses) < 2:
        raise ValueError(
            "Evaluation must contain at least "
            "2 weaknesses or evidence gaps."
        )

    # Improvements should not be empty
    if len(evaluation.improvements) < 2:
        raise ValueError(
            "Evaluation must contain at least "
            "2 practical improvements."
        )


# ============================================================
# CANDIDATE EVALUATOR
# ============================================================

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
6. Missing information means "not evidenced", not necessarily
   poor ability.


IMPORTANT EVIDENCE RULES:

- Designation and years of experience are context only.

- Do NOT use designation alone as evidence of:
  leadership,
  strategic responsibility,
  stakeholder altitude,
  scope,
  or business impact.

- Do NOT assume that because someone is a Director,
  VP, Manager, or another senior title that they necessarily
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


EVIDENCE INTERPRETATION RULES:

- Do not treat evidence of scope as automatic evidence
  of capability quality.

- For example, managing a large team demonstrates
  leadership scope, but does not automatically demonstrate
  coaching quality, mentoring ability, talent development,
  retention, or team performance.

- Do not use an achievement from one capability as proof
  of another capability unless the candidate profile
  explicitly supports the relationship.

- For example, revenue growth does not automatically prove
  strong people leadership.

- Do not invent causal relationships.

- If the profile states that revenue increased by 20%,
  do not claim that coaching, transformation, leadership,
  or another activity caused that increase unless the
  candidate profile explicitly establishes that relationship.


SUMMARY REQUIREMENTS:

STRENGTHS:

- Return at least 2 specific strengths.
- Every strength must be supported by explicit candidate evidence.
- Do not use designation or years of experience alone as a strength.
- Prefer demonstrated achievements, scale, outcomes,
  responsibilities or capabilities.


WEAKNESSES:

- Return at least 2 weaknesses OR evidence gaps.
- Missing evidence must be described as an evidence gap,
  not automatically as candidate weakness.
- Do not invent weaknesses.

For example:

Good:
"Team development outcomes are not clearly evidenced."

Bad:
"The candidate is poor at team development."

unless the candidate profile explicitly supports that conclusion.


IMPROVEMENTS:

- Return at least 2 practical improvements.
- Improvements should address capability gaps,
  evidence gaps, or areas where the candidate could
  demonstrate stronger alignment with the benchmark.
- Avoid generic advice.


OVERALL ANALYSIS:

- Summarize the candidate's overall alignment with the benchmark.
- Clearly distinguish demonstrated strengths from areas
  that are simply not evidenced.
- Do not introduce evidence that was not used in the
  dimension evaluations.


IMPORTANT:

- Do not add new benchmark dimensions.
- Do not remove benchmark dimensions.
- Use the benchmark dimensions exactly as supplied.
- Consider designation, experience, industry and geography
  when interpreting the strength of the evidence.
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

    evaluation = BenchmarkEvaluation.model_validate_json(
        response.text
    )

    validate_evaluation(
        evaluation,
        function_benchmark,
    )

    return evaluation