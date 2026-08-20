from app.models.role_benchmark import RoleBenchmark
from app.models.benchmark_score import BenchmarkEvaluation


def calculate_weighted_score(
    evaluation: BenchmarkEvaluation,
    function_benchmark: RoleBenchmark,
) -> float:

    # Create a lookup dictionary:
    # dimension name -> weight
    weights = {}

    for dimension in function_benchmark.dimensions:
        weights[dimension.name] = dimension.weight


    # Store each weighted score here
    weighted_scores = []


    # Go through every score returned by Gemini
    for result in evaluation.dimension_scores:

        # Example:
        # result.dimension = "FP&A Core Depth"
        # weights["FP&A Core Depth"] = 0.20
        weight = weights[result.dimension]

        # Example:
        # score = 7
        # weight = 0.20
        # weighted_score = 1.4
        weighted_score = (
            result.score * weight
        )

        weighted_scores.append(
            weighted_score
        )


    # Add all weighted scores
    final_score = sum(
        weighted_scores
    )

    return round(final_score, 2)