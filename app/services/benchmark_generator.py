# app/services/benchmark_generator.py

import logging
import time

from app.models.candidate_profile import CandidateProfile
from app.models.role_benchmark import RoleBenchmark

from app.services.benchmark_validator import (
    validate_benchmark,
)

from app.services.gemini_service import (
    generate_structured_response,
)


# ============================================================
# LOGGING
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# DYNAMIC BENCHMARK GENERATOR
# ============================================================

def generate_benchmark(
    candidate_profile: CandidateProfile,
) -> RoleBenchmark:

    total_start = time.perf_counter()

    logger.info("=" * 60)
    logger.info("Dynamic benchmark generation started.")
    logger.info("=" * 60)

    try:

        # ====================================================
        # STEP 1 — BUILD PROMPT
        # ====================================================

        prompt_start = time.perf_counter()

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


Your task is to determine WHAT should be evaluated
for a strong professional with this function and context.


REQUIREMENTS:

1. Create between 5 and 8 meaningful evaluation dimensions.

2. Dimensions must be relevant to:

   - function
   - seniority
   - experience
   - industry
   - geography

3. Each dimension must contain:

   - a clear name
   - a clear description
   - a weight

4. All dimension weights must add up to exactly 1.0.

5. Avoid overlapping dimensions.

6. Do NOT evaluate or score this specific candidate.

7. Do NOT use candidate-specific achievements such as:

   - team size
   - portfolio handled
   - business impact
   - skills
   - budget handled
   - transformation achievements

   to make the benchmark easier or harder for this candidate.

8. The benchmark should represent what a strong professional
   in this context should normally be evaluated on.


EVALUATION CRITERIA:

For each benchmark dimension:

- Create 3 to 6 evaluation criteria.

- Each criterion must represent a distinct aspect
  of the dimension.

- Avoid duplicate or overlapping criteria.

- Criteria should be specific enough that a candidate
  can later be assessed against them.

- Do not include candidate-specific achievements.

- Criteria must reflect the role context:

  function,
  designation,
  experience,
  industry,
  geography.


IMPORTANT:

You are designing the benchmark.

You are NOT evaluating the candidate.

Return the benchmark using the required RoleBenchmark schema.
"""

        prompt_elapsed = (
            time.perf_counter()
            - prompt_start
        )

        logger.info(
            "Benchmark prompt built in %.4f seconds.",
            prompt_elapsed,
        )

        logger.info(
            "Benchmark prompt size: %d characters.",
            len(prompt),
        )


        # ====================================================
        # STEP 2 — GEMINI WITH RETRY + FALLBACK
        # ====================================================

        logger.info(
            "Sending benchmark generation "
            "request to AI service..."
        )

        llm_start = time.perf_counter()

        response = generate_structured_response(
            prompt=prompt,
            schema=RoleBenchmark,
        )

        llm_elapsed = (
            time.perf_counter()
            - llm_start
        )

        logger.info(
            "Benchmark AI call completed "
            "in %.2f seconds.",
            llm_elapsed,
        )


        # ====================================================
        # STEP 3 — RESPONSE CHECK
        # ====================================================

        response_text = response.text

        if not response_text:

            raise ValueError(
                "AI service returned "
                "an empty benchmark."
            )

        logger.info(
            "Benchmark response size: "
            "%d characters.",
            len(response_text),
        )


        # ====================================================
        # STEP 4 — PYDANTIC
        # ====================================================

        validation_start = time.perf_counter()

        benchmark = (
            RoleBenchmark.model_validate_json(
                response_text
            )
        )

        logger.info(
            "RoleBenchmark Pydantic validation "
            "completed in %.4f seconds.",
            (
                time.perf_counter()
                - validation_start
            ),
        )


        # ====================================================
        # STEP 5 — BUSINESS VALIDATION
        # ====================================================

        logger.info(
            "Starting benchmark business validation."
        )

        business_validation_start = (
            time.perf_counter()
        )

        validate_benchmark(
            benchmark
        )

        logger.info(
            "Benchmark business validation "
            "completed in %.4f seconds.",
            (
                time.perf_counter()
                - business_validation_start
            ),
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
            "Dynamic benchmark generation COMPLETE "
            "in %.2f seconds.",
            total_elapsed,
        )

        logger.info("=" * 60)

        return benchmark


    except Exception:

        total_elapsed = (
            time.perf_counter()
            - total_start
        )

        logger.exception(
            "Dynamic benchmark generation FAILED "
            "after %.2f seconds.",
            total_elapsed,
        )

        raise