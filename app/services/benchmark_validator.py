from app.models.role_benchmark import RoleBenchmark


def validate_benchmark(
    benchmark: RoleBenchmark,
) -> None:

    # Must have 5–8 dimensions
    if not 5 <= len(benchmark.dimensions) <= 8:
        raise ValueError(
            f"Benchmark must contain 5 to 8 dimensions. "
            f"Got {len(benchmark.dimensions)}."
        )

    # Every weight must be valid
    for dimension in benchmark.dimensions:

        if dimension.weight <= 0:
            raise ValueError(
                f"{dimension.name} has invalid weight "
                f"{dimension.weight}"
            )

        if dimension.weight > 1:
            raise ValueError(
                f"{dimension.name} has invalid weight "
                f"{dimension.weight}"
            )

    # All weights must total 1.0
    total_weight = sum(
        dimension.weight
        for dimension in benchmark.dimensions
    )

    if abs(total_weight - 1.0) > 0.001:
        raise ValueError(
            f"Benchmark weights must total 1.0. "
            f"Got {total_weight}"
        )