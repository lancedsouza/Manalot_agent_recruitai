# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# from app.models.candidate_profile import CandidateProfile
# from app.models.role_benchmark import RoleBenchmark
# from app.models.benchmark_score import BenchmarkEvaluation


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
# # VALIDATION
# # ============================================================

# def validate_evaluation(
#     evaluation: BenchmarkEvaluation,
#     benchmark: RoleBenchmark,
# ) -> None:

#     # Every benchmark dimension should have a score
#     if len(evaluation.dimension_scores) != len(
#         benchmark.dimensions
#     ):
#         raise ValueError(
#             "Evaluation does not contain a score "
#             "for every benchmark dimension."
#         )

#     # Strengths should not be empty
#     if len(evaluation.strengths) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 evidence-based strengths."
#         )

#     # Weaknesses / evidence gaps should not be empty
#     if len(evaluation.weaknesses) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 weaknesses or evidence gaps."
#         )

#     # Improvements should not be empty
#     if len(evaluation.improvements) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 practical improvements."
#         )


# # ============================================================
# # CANDIDATE EVALUATOR
# # ============================================================

# def eval_candidate(
#     candidate_profile: CandidateProfile,
#     function_benchmark: RoleBenchmark,
# ) -> BenchmarkEvaluation:

#     prompt = f"""
# You are evaluating a candidate against a predefined
# professional benchmark.

# CANDIDATE PROFILE:

# {candidate_profile.model_dump_json(indent=2)}

# BENCHMARK:

# {function_benchmark.model_dump_json(indent=2)}

# INSTRUCTIONS:

# Evaluate the candidate on EVERY benchmark dimension.

# For each dimension:

# 1. Give a score from 0 to 10.
# 2. Use only evidence available in the candidate profile.
# 3. List the evidence supporting the score.
# 4. Explain briefly why the evidence justifies the score.
# 5. Do not invent missing achievements or responsibilities.
# 6. Missing information means "not evidenced", not necessarily
#    poor ability.
# 7. Identify what actions or outcomes demonstrate the capability.

# 8. Identify important missing information as evidence gaps.Do not treat missing evidence as proof of poor capability..
# 9.Explain why the available evidence, demonstrated outcomes,
# and evidence gaps justify the specific score given,
# including why the evidence does not support a materially higher score.

# IMPORTANT EVIDENCE RULES:

# - Designation and years of experience are context only.

# - Do NOT use designation alone as evidence of:
#   leadership,
#   strategic responsibility,
#   stakeholder altitude,
#   scope,
#   or business impact.

# - Do NOT assume that because someone is a Director,
#   VP, Manager, or another senior title that they necessarily
#   demonstrated the expected capability.

# - Prefer explicit evidence such as:
#   team size,
#   revenue owned,
#   portfolio size,
#   budget ownership,
#   target attainment,
#   markets handled,
#   deal complexity,
#   stakeholder level,
#   measurable business outcomes,
#   transformation ownership.

# - Skills listed without supporting experience are weaker
#   evidence than demonstrated achievements.

# - If something is implied but not explicitly supported,
#   state "not clearly evidenced" and score accordingly.

# - Do not invent evidence.


# EVIDENCE INTERPRETATION RULES:

# - Do not treat evidence of scope as automatic evidence
#   of capability quality.

# - For example, managing a large team demonstrates
#   leadership scope, but does not automatically demonstrate
#   coaching quality, mentoring ability, talent development,
#   retention, or team performance.

# - Do not use an achievement from one capability as proof
#   of another capability unless the candidate profile
#   explicitly supports the relationship.

# - For example, revenue growth does not automatically prove
#   strong people leadership.

# - Do not invent causal relationships.

# - If the profile states that revenue increased by 20%,
#   do not claim that coaching, transformation, leadership,
#   or another activity caused that increase unless the
#   candidate profile explicitly establishes that relationship.


# SUMMARY REQUIREMENTS:

# STRENGTHS:

# - Return at least 2 specific strengths.
# - Every strength must be supported by explicit candidate evidence.
# - Do not use designation or years of experience alone as a strength.
# - Prefer demonstrated achievements, scale, outcomes,
#   responsibilities or capabilities.


# WEAKNESSES:

# - Return at least 2 weaknesses OR evidence gaps.
# - Missing evidence must be described as an evidence gap,
#   not automatically as candidate weakness.
# - Do not invent weaknesses.

# For example:

# Good:
# "Team development outcomes are not clearly evidenced."

# Bad:
# "The candidate is poor at team development."

# unless the candidate profile explicitly supports that conclusion.


# IMPROVEMENTS:

# - Return at least 2 practical improvements.
# - Improvements should address capability gaps,
#   evidence gaps, or areas where the candidate could
#   demonstrate stronger alignment with the benchmark.
# - Avoid generic advice.


# OVERALL ANALYSIS:

# - Summarize the candidate's overall alignment with the benchmark.
# - Clearly distinguish demonstrated strengths from areas
#   that are simply not evidenced.
# - Do not introduce evidence that was not used in the
#   dimension evaluations.


# IMPORTANT:

# - Do not add new benchmark dimensions.
# - Do not remove benchmark dimensions.
# - Use the benchmark dimensions exactly as supplied.
# - Consider designation, experience, industry and geography
#   when interpreting the strength of the evidence.
# """

#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             temperature=0,
#             response_mime_type="application/json",
#             response_schema=BenchmarkEvaluation,
#         ),
#     )
#     print("\n===== RAW GEMINI RESPONSE =====")
#     print(repr(response.text))
#     print("================================\n")

#     evaluation = BenchmarkEvaluation.model_validate_json(
#         response.text
#     )

#     validate_evaluation(
#         evaluation,
#         function_benchmark,
#     )

#     return evaluation


"""using nvidia API"""
# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from openai import OpenAI

# from app.models.candidate_profile import CandidateProfile
# from app.models.role_benchmark import RoleBenchmark
# from app.models.benchmark_score import BenchmarkEvaluation


# # ============================================================
# # CONFIGURATION
# # ============================================================

# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# ENV_PATH = PROJECT_ROOT / ".env"

# load_dotenv(ENV_PATH)

# api_key = os.getenv("NVIDIA_API_KEY")

# if not api_key:
#     raise ValueError(
#         f"NVIDIA_API_KEY not found in {ENV_PATH}"
#     )


# # Initialize NVIDIA NIM client with OpenAI-compatible interface
# client = OpenAI(
#     base_url="https://integrate.api.nvidia.com/v1",
#     api_key=api_key,
# )

# # Using a high-quality NVIDIA model (you can change this)
# MODEL_NAME = "nvidia/nemotron-3.5-lightning-30b-a3b"  # or "meta/llama-3.1-70b-instruct" etc.


# # ============================================================
# # VALIDATION
# # ============================================================

# def validate_evaluation(
#     evaluation: BenchmarkEvaluation,
#     benchmark: RoleBenchmark,
# ) -> None:

#     # Every benchmark dimension should have a score
#     if len(evaluation.dimension_scores) != len(
#         benchmark.dimensions
#     ):
#         raise ValueError(
#             "Evaluation does not contain a score "
#             "for every benchmark dimension."
#         )

#     # Strengths should not be empty
#     if len(evaluation.strengths) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 evidence-based strengths."
#         )

#     # Weaknesses / evidence gaps should not be empty
#     if len(evaluation.weaknesses) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 weaknesses or evidence gaps."
#         )

#     # Improvements should not be empty
#     if len(evaluation.improvements) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 practical improvements."
#         )


# # ============================================================
# # CANDIDATE EVALUATOR
# # ============================================================

# def eval_candidate(
#     candidate_profile: CandidateProfile,
#     function_benchmark: RoleBenchmark,
# ) -> BenchmarkEvaluation:

#     prompt = f"""
# You are evaluating a candidate against a predefined
# professional benchmark.

# CANDIDATE PROFILE:

# {candidate_profile.model_dump_json(indent=2)}

# BENCHMARK:

# {function_benchmark.model_dump_json(indent=2)}

# INSTRUCTIONS:

# Evaluate the candidate on EVERY benchmark dimension.

# For each dimension:

# 1. Give a score from 0 to 10.
# 2. Use only evidence available in the candidate profile.
# 3. List the evidence supporting the score.
# 4. Explain briefly why the evidence justifies the score.
# 5. Do not invent missing achievements or responsibilities.
# 6. Missing information means "not evidenced", not necessarily
#    poor ability.
# 7. Identify what actions or outcomes demonstrate the capability.

# 8. Identify important missing information as evidence gaps.Do not treat missing evidence as proof of poor capability..
# 9.Explain why the available evidence, demonstrated outcomes,
# and evidence gaps justify the specific score given,
# including why the evidence does not support a materially higher score.

# IMPORTANT EVIDENCE RULES:

# - Designation and years of experience are context only.

# - Do NOT use designation alone as evidence of:
#   leadership,
#   strategic responsibility,
#   stakeholder altitude,
#   scope,
#   or business impact.

# - Do NOT assume that because someone is a Director,
#   VP, Manager, or another senior title that they necessarily
#   demonstrated the expected capability.

# - Prefer explicit evidence such as:
#   team size,
#   revenue owned,
#   portfolio size,
#   budget ownership,
#   target attainment,
#   markets handled,
#   deal complexity,
#   stakeholder level,
#   measurable business outcomes,
#   transformation ownership.

# - Skills listed without supporting experience are weaker
#   evidence than demonstrated achievements.

# - If something is implied but not explicitly supported,
#   state "not clearly evidenced" and score accordingly.

# - Do not invent evidence.


# EVIDENCE INTERPRETATION RULES:

# - Do not treat evidence of scope as automatic evidence
#   of capability quality.

# - For example, managing a large team demonstrates
#   leadership scope, but does not automatically demonstrate
#   coaching quality, mentoring ability, talent development,
#   retention, or team performance.

# - Do not use an achievement from one capability as proof
#   of another capability unless the candidate profile
#   explicitly supports the relationship.

# - For example, revenue growth does not automatically prove
#   strong people leadership.

# - Do not invent causal relationships.

# - If the profile states that revenue increased by 20%,
#   do not claim that coaching, transformation, leadership,
#   or another activity caused that increase unless the
#   candidate profile explicitly establishes that relationship.


# SUMMARY REQUIREMENTS:

# STRENGTHS:

# - Return at least 2 specific strengths.
# - Every strength must be supported by explicit candidate evidence.
# - Do not use designation or years of experience alone as a strength.
# - Prefer demonstrated achievements, scale, outcomes,
#   responsibilities or capabilities.


# WEAKNESSES:

# - Return at least 2 weaknesses OR evidence gaps.
# - Missing evidence must be described as an evidence gap,
#   not automatically as candidate weakness.
# - Do not invent weaknesses.

# For example:

# Good:
# "Team development outcomes are not clearly evidenced."

# Bad:
# "The candidate is poor at team development."

# unless the candidate profile explicitly supports that conclusion.


# IMPROVEMENTS:

# - Return at least 2 practical improvements.
# - Improvements should address capability gaps,
#   evidence gaps, or areas where the candidate could
#   demonstrate stronger alignment with the benchmark.
# - Avoid generic advice.


# OVERALL ANALYSIS:

# - Summarize the candidate's overall alignment with the benchmark.
# - Clearly distinguish demonstrated strengths from areas
#   that are simply not evidenced.
# - Do not introduce evidence that was not used in the
#   dimension evaluations.


# IMPORTANT:

# - Do not add new benchmark dimensions.
# - Do not remove benchmark dimensions.
# - Use the benchmark dimensions exactly as supplied.
# - Consider designation, experience, industry and geography
#   when interpreting the strength of the evidence.

# IMPORTANT: Return your response as a valid JSON object that matches the BenchmarkEvaluation schema.
# """

#     # NVIDIA NIM API call using OpenAI-compatible interface
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": "You are an AI assistant that evaluates candidates against professional benchmarks. Always respond with valid JSON."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0,
#         max_tokens=4096,  # Adjust based on model context window
#         response_format={"type": "json_object"}  # Note: This may not work for all models
#     )

#     # Extract the JSON response
#     response_text = response.choices[0].message.content
    
#     # Parse the JSON response
#     evaluation = BenchmarkEvaluation.model_validate_json(
#         response_text
#     )

#     validate_evaluation(
#         evaluation,
#         function_benchmark,
#     )

#     return evaluation
"""with logger and gemini api"""
# import logging
# import os
# import time
# from pathlib import Path

# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# from pydantic import ValidationError

# from app.models.candidate_profile import CandidateProfile
# from app.models.role_benchmark import RoleBenchmark
# from app.models.benchmark_score import BenchmarkEvaluation


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
# # VALIDATION
# # ============================================================

# def validate_evaluation(
#     evaluation: BenchmarkEvaluation,
#     benchmark: RoleBenchmark,
# ) -> None:

#     logger.info(
#         "Starting business-rule validation."
#     )

#     start = time.perf_counter()

#     # Every benchmark dimension should have a score
#     if len(evaluation.dimension_scores) != len(
#         benchmark.dimensions
#     ):
#         raise ValueError(
#             "Evaluation does not contain a score "
#             "for every benchmark dimension."
#         )

#     # Strengths
#     if len(evaluation.strengths) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 evidence-based strengths."
#         )

#     # Weaknesses
#     if len(evaluation.weaknesses) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 weaknesses or evidence gaps."
#         )

#     # Improvements
#     if len(evaluation.improvements) < 2:
#         raise ValueError(
#             "Evaluation must contain at least "
#             "2 practical improvements."
#         )

#     elapsed = time.perf_counter() - start

#     logger.info(
#         "Business validation completed in %.4f seconds.",
#         elapsed,
#     )


# # ============================================================
# # CANDIDATE EVALUATOR
# # ============================================================

# def eval_candidate(
#     candidate_profile: CandidateProfile,
#     function_benchmark: RoleBenchmark,
# ) -> BenchmarkEvaluation:

#     # TOTAL timer
#     total_start = time.perf_counter()

#     logger.info("=" * 60)
#     logger.info("Candidate evaluation started.")
#     logger.info("=" * 60)

#     try:

#         # ====================================================
#         # STEP 1 — SERIALIZE CANDIDATE
#         # ====================================================

#         start = time.perf_counter()

#         candidate_json = (
#             candidate_profile.model_dump_json()
#         )

#         elapsed = time.perf_counter() - start

#         logger.info(
#             "Candidate profile serialized in %.4f seconds.",
#             elapsed,
#         )

#         logger.info(
#             "Candidate profile size: %d characters.",
#             len(candidate_json),
#         )


#         # ====================================================
#         # STEP 2 — SERIALIZE BENCHMARK
#         # ====================================================

#         start = time.perf_counter()

#         benchmark_json = (
#             function_benchmark.model_dump_json()
#         )

#         elapsed = time.perf_counter() - start

#         logger.info(
#             "Benchmark serialized in %.4f seconds.",
#             elapsed,
#         )

#         logger.info(
#             "Benchmark size: %d characters.",
#             len(benchmark_json),
#         )

#         logger.info(
#             "Benchmark dimensions: %d.",
#             len(function_benchmark.dimensions),
#         )


#         # ====================================================
#         # STEP 3 — BUILD PROMPT
#         # ====================================================

#         start = time.perf_counter()

#         prompt = f"""
# You are evaluating a candidate against a predefined
# professional benchmark.

# CANDIDATE PROFILE:

# {candidate_json}

# BENCHMARK:

# {benchmark_json}


# INSTRUCTIONS:

# Evaluate the candidate on EVERY benchmark dimension.

# For each dimension:

# 1. Give a score from 0 to 10.

# 2. Use only evidence available in the candidate profile.

# 3. List evidence supporting the score.

# 4. Explain why the evidence justifies the score.

# 5. Do not invent missing achievements or responsibilities.

# 6. Missing information means "not evidenced",
#    not necessarily poor ability.

# 7. Identify actions or outcomes that demonstrate
#    the capability.

# 8. Identify important missing information as
#    evidence gaps.

# 9. Explain why the available evidence and evidence
#    gaps justify the score, including why the evidence
#    does not support a materially higher score.


# IMPORTANT EVIDENCE RULES:

# - Designation and years of experience are context only.

# - Do not use designation alone as evidence of
#   leadership, strategic responsibility,
#   stakeholder altitude, scope or business impact.

# - Do not assume that a Director, VP, Manager
#   or another senior title automatically demonstrates
#   the expected capability.

# - Prefer explicit evidence such as:
#   team size,
#   revenue owned,
#   portfolio size,
#   budget ownership,
#   target attainment,
#   markets handled,
#   deal complexity,
#   stakeholder level,
#   measurable business outcomes,
#   transformation ownership.

# - Skills listed without supporting experience
#   are weaker evidence than demonstrated achievements.

# - If something is implied but not explicitly supported,
#   state "not clearly evidenced".

# - Do not invent evidence.


# EVIDENCE INTERPRETATION:

# - Scope is not automatically evidence of quality.

# - A large team demonstrates leadership scope,
#   but does not automatically demonstrate coaching,
#   mentoring, talent development or retention.

# - Do not use evidence from one capability as proof
#   of another unless explicitly supported.

# - Do not invent causal relationships.


# STRENGTHS:

# - Return at least 2 specific strengths.

# - Every strength must be supported by explicit
#   candidate evidence.

# - Do not use designation or experience alone
#   as a strength.


# WEAKNESSES:

# - Return at least 2 weaknesses OR evidence gaps.

# - Missing evidence must be described as an
#   evidence gap, not automatically as a weakness.

# - Do not invent weaknesses.


# IMPROVEMENTS:

# - Return at least 2 practical improvements.

# - Improvements should address capability gaps
#   or evidence gaps.

# - Avoid generic advice.


# OVERALL ANALYSIS:

# - Summarize overall alignment with the benchmark.

# - Clearly distinguish demonstrated strengths
#   from areas that are not evidenced.

# - Do not introduce new evidence.


# IMPORTANT:

# - Do not add benchmark dimensions.

# - Do not remove benchmark dimensions.

# - Use benchmark dimensions exactly as supplied.
# """

#         elapsed = time.perf_counter() - start

#         logger.info(
#             "Prompt created in %.4f seconds.",
#             elapsed,
#         )

#         logger.info(
#             "Final prompt size: %d characters.",
#             len(prompt),
#         )


#         # ====================================================
#         # STEP 4 — GEMINI CALL
#         # ====================================================

#         logger.info(
#             "Sending candidate evaluation to Gemini..."
#         )

#         gemini_start = time.perf_counter()

#         try:

#             response = client.models.generate_content(
#                 model=MODEL_NAME,
#                 contents=prompt,
#                 config=types.GenerateContentConfig(
#                     temperature=0,
#                     response_mime_type="application/json",
#                     response_schema=BenchmarkEvaluation,
#                 ),
#             )

#         except Exception:

#             gemini_elapsed = (
#                 time.perf_counter()
#                 - gemini_start
#             )

#             logger.exception(
#                 "Gemini API call FAILED after %.2f seconds.",
#                 gemini_elapsed,
#             )

#             raise


#         gemini_elapsed = (
#             time.perf_counter()
#             - gemini_start
#         )

#         logger.info(
#             "Gemini returned in %.2f seconds.",
#             gemini_elapsed,
#         )


#         # ====================================================
#         # STEP 5 — INSPECT RESPONSE
#         # ====================================================

#         response_text = response.text

#         if response_text is None:

#             logger.error(
#                 "Gemini response.text is None."
#             )

#             raise ValueError(
#                 "Gemini returned no response text."
#             )


#         logger.info(
#             "Gemini response size: %d characters.",
#             len(response_text),
#         )


#         # IMPORTANT:
#         # Do not normally dump candidate data into logs
#         # in production because resumes contain PII.
#         #
#         # For debugging JSON format, showing only the first
#         # 300 characters is usually enough.

#         logger.info(
#             "Gemini response preview: %r",
#             response_text[:300],
#         )


#         # ====================================================
#         # STEP 6 — PYDANTIC JSON VALIDATION
#         # ====================================================

#         logger.info(
#             "Starting Pydantic validation..."
#         )

#         validation_start = time.perf_counter()

#         try:

#             evaluation = (
#                 BenchmarkEvaluation.model_validate_json(
#                     response_text
#                 )
#             )

#         except ValidationError:

#             validation_elapsed = (
#                 time.perf_counter()
#                 - validation_start
#             )

#             logger.exception(
#                 "Pydantic validation FAILED "
#                 "after %.4f seconds.",
#                 validation_elapsed,
#             )

#             logger.error(
#                 "Invalid Gemini response starts with: %r",
#                 response_text[:500],
#             )

#             raise


#         validation_elapsed = (
#             time.perf_counter()
#             - validation_start
#         )

#         logger.info(
#             "Pydantic validation completed "
#             "in %.4f seconds.",
#             validation_elapsed,
#         )


#         # ====================================================
#         # STEP 7 — BUSINESS VALIDATION
#         # ====================================================

#         try:

#             validate_evaluation(
#                 evaluation,
#                 function_benchmark,
#             )

#         except ValueError:

#             logger.exception(
#                 "Business-rule validation FAILED."
#             )

#             raise


#         # ====================================================
#         # FINISHED
#         # ====================================================

#         total_elapsed = (
#             time.perf_counter()
#             - total_start
#         )

#         logger.info("=" * 60)

#         logger.info(
#             "Candidate evaluation COMPLETE "
#             "in %.2f seconds.",
#             total_elapsed,
#         )

#         logger.info("=" * 60)

#         return evaluation


#     # ========================================================
#     # CATCH ANY FAILURE FROM THE WHOLE PIPELINE
#     # ========================================================

#     except Exception:

#         total_elapsed = (
#             time.perf_counter()
#             - total_start
#         )

#         logger.exception(
#             "Candidate evaluation FAILED "
#             "after %.2f seconds.",
#             total_elapsed,
#         )

#         raise

"""New with gemini lite"""

# app/services/candidate_evaluator.py

import logging
import time

from pydantic import ValidationError

from app.models.candidate_profile import CandidateProfile
from app.models.role_benchmark import RoleBenchmark
from app.models.benchmark_score import BenchmarkEvaluation

from app.services.gemini_service import (
    generate_structured_response,
)


# ============================================================
# LOGGING
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# BUSINESS VALIDATION
# ============================================================

def validate_evaluation(
    evaluation: BenchmarkEvaluation,
    benchmark: RoleBenchmark,
) -> None:

    logger.info(
        "Starting business validation."
    )

    start = time.perf_counter()


    if (
        len(evaluation.dimension_scores)
        != len(benchmark.dimensions)
    ):

        raise ValueError(
            "Evaluation does not contain "
            "a score for every benchmark dimension."
        )


    if len(evaluation.strengths) < 2:

        raise ValueError(
            "Evaluation requires at least "
            "2 strengths."
        )


    if len(evaluation.weaknesses) < 2:

        raise ValueError(
            "Evaluation requires at least "
            "2 weaknesses/evidence gaps."
        )


    if len(evaluation.improvements) < 2:

        raise ValueError(
            "Evaluation requires at least "
            "2 improvements."
        )


    logger.info(
        "Business validation complete "
        "in %.4f seconds.",
        (
            time.perf_counter()
            - start
        ),
    )


# ============================================================
# CANDIDATE EVALUATION
# ============================================================

def eval_candidate(
    candidate_profile: CandidateProfile,
    function_benchmark: RoleBenchmark,
) -> BenchmarkEvaluation:

    total_start = (
        time.perf_counter()
    )


    logger.info("=" * 60)

    logger.info(
        "Candidate evaluation started."
    )

    logger.info("=" * 60)


    try:

        # ====================================================
        # SERIALIZATION
        # ====================================================

        candidate_json = (
            candidate_profile.model_dump_json()
        )

        benchmark_json = (
            function_benchmark.model_dump_json()
        )


        logger.info(
            "Candidate profile size: "
            "%d characters.",
            len(candidate_json),
        )


        logger.info(
            "Benchmark size: "
            "%d characters.",
            len(benchmark_json),
        )


        logger.info(
            "Benchmark dimensions: %d",
            len(
                function_benchmark.dimensions
            ),
        )


        # ====================================================
        # PROMPT
        # ====================================================

        prompt = f"""
You are evaluating a candidate against a predefined
professional benchmark.

CANDIDATE PROFILE:

{candidate_json}


BENCHMARK:

{benchmark_json}


Evaluate the candidate on EVERY benchmark dimension.


FOR EACH DIMENSION:

1. Give a score from 0 to 10.

2. Use only explicit evidence contained in
   the candidate profile.

3. List the evidence supporting the score.

4. Explain why the evidence justifies the score.

5. Identify important missing evidence.

6. Explain why the evidence does not support
   a materially higher score.


EVIDENCE RULES:

- Never invent evidence.

- Missing information means "not evidenced",
  not proof of poor capability.

- Designation and years of experience are
  context only.

- Do NOT use designation alone as evidence
  of leadership, strategy, scope,
  stakeholder altitude or business impact.

- Do not assume that Director, VP,
  General Manager, Manager or other
  senior titles prove capability.

- Prefer explicit evidence such as:

  team size,
  revenue responsibility,
  portfolio size,
  budget ownership,
  markets handled,
  stakeholder level,
  deal complexity,
  measurable outcomes,
  transformation ownership.

- Skills without demonstrated application
  are weaker evidence.

- Evidence of scope is not automatically
  evidence of quality.

- Do not infer causal relationships
  that are not explicitly supported.

Example:

If revenue increased by 20%,
do NOT claim leadership or coaching
caused the increase unless the profile
explicitly establishes that relationship.


STRENGTHS:

- Return at least 2 strengths.

- Every strength must be supported by
  explicit candidate evidence.


WEAKNESSES / EVIDENCE GAPS:

- Return at least 2.

- Missing evidence must be described as
  an evidence gap rather than automatically
  as poor capability.


IMPROVEMENTS:

- Return at least 2 practical improvements.

- Improvements should address capability
  gaps or evidence gaps.

- Avoid generic advice.


OVERALL ANALYSIS:

- Summarize overall alignment.

- Clearly distinguish demonstrated strengths
  from areas not evidenced.

- Do not introduce new evidence.


BENCHMARK RULES:

- Do not add benchmark dimensions.

- Do not remove benchmark dimensions.

- Use benchmark dimensions exactly
  as supplied.
"""


        logger.info(
            "Evaluation prompt size: "
            "%d characters.",
            len(prompt),
        )


        # ====================================================
        # GEMINI + FAILOVER
        # ====================================================

        logger.info(
            "Sending candidate evaluation "
            "to AI service..."
        )


        llm_start = (
            time.perf_counter()
        )


        try:

            response = (
                generate_structured_response(
                    prompt=prompt,
                    schema=BenchmarkEvaluation,
                )
            )

        except Exception:

            logger.exception(
                "Candidate AI evaluation failed "
                "after %.2f seconds.",
                (
                    time.perf_counter()
                    - llm_start
                ),
            )

            raise


        logger.info(
            "Candidate AI call returned "
            "in %.2f seconds.",
            (
                time.perf_counter()
                - llm_start
            ),
        )


        # ====================================================
        # RESPONSE
        # ====================================================

        response_text = (
            response.text
        )


        if not response_text:

            raise ValueError(
                "AI service returned "
                "an empty evaluation."
            )


        logger.info(
            "Evaluation response size: "
            "%d characters.",
            len(response_text),
        )


        logger.debug(
            "Evaluation response preview: %r",
            response_text[:300],
        )


        # ====================================================
        # PYDANTIC
        # ====================================================

        validation_start = (
            time.perf_counter()
        )


        try:

            evaluation = (
                BenchmarkEvaluation
                .model_validate_json(
                    response_text
                )
            )

        except ValidationError:

            logger.exception(
                "BenchmarkEvaluation "
                "Pydantic validation failed."
            )

            logger.error(
                "Response starts with: %r",
                response_text[:500],
            )

            raise


        logger.info(
            "Pydantic validation: %.4fs",
            (
                time.perf_counter()
                - validation_start
            ),
        )


        # ====================================================
        # BUSINESS VALIDATION
        # ====================================================

        validate_evaluation(
            evaluation,
            function_benchmark,
        )


        # ====================================================
        # COMPLETE
        # ====================================================

        elapsed = (
            time.perf_counter()
            - total_start
        )


        logger.info("=" * 60)

        logger.info(
            "Candidate evaluation COMPLETE "
            "in %.2f seconds.",
            elapsed,
        )

        logger.info("=" * 60)


        return evaluation


    except Exception:

        logger.exception(
            "Candidate evaluation FAILED "
            "after %.2f seconds.",
            (
                time.perf_counter()
                - total_start
            ),
        )

        raise