from app.benchmarks.fpa_benchmark import FPA_BENCHMARK
from app.models.role_benchmark import RoleBenchmark


def get_existing_benchmark(
    function_name: str,
) -> RoleBenchmark | None:

    normalized = function_name.strip().lower()

    if normalized in {
        "fp&a",
        "financial planning and analysis",
        "financial planning & analysis",
    }:
        return FPA_BENCHMARK

    return None