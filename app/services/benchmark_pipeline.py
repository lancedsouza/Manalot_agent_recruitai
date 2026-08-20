from app.models.candidate_profile import CandidateProfile
from app.services.benchmark_selector import get_existing_benchmark
from app.services.benchmark_generator import generate_benchmark
from app.services.candidate_evaluator import eval_candidate
from app.services.score_calculator import calculate_weighted_score


def benchmark_candidate(
    candidate_profile: CandidateProfile,
):

    # 1. Look for a validated/stored benchmark
    benchmark = get_existing_benchmark(
        candidate_profile.function
    )

    # 2. If none exists, generate one
    if benchmark is None:
        benchmark = generate_benchmark(
            candidate_profile
        )

    # 3. Evaluate candidate against benchmark
    evaluation = eval_candidate(
        candidate_profile=candidate_profile,
        function_benchmark=benchmark,
    )

    # 4. Calculate weighted final score
    final_score = calculate_weighted_score(
        evaluation=evaluation,
        function_benchmark=benchmark,
    )

    # 5. Return result
    return {
        "candidate": candidate_profile.name,
        "function": candidate_profile.function,
        "benchmark": benchmark,
        "final_score": final_score,
        "evaluation": evaluation,
    }