from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.models.candidate_profile import CandidateProfile
from app.models.role_benchmark import RoleBenchmark
from app.models.benchmark_score import BenchmarkEvaluation



class BenchmarkState(TypedDict, total=False):

    candidate_profile: CandidateProfile

    benchmark: RoleBenchmark

    evaluation: BenchmarkEvaluation

    final_score: float

state=StateGraph(BenchmarkState)
from app.agents.benchmark_state import BenchmarkState

from app.services.benchmark_selector import get_existing_benchmark
from app.services.benchmark_generator import generate_benchmark
from app.services.candidate_evaluator import eval_candidate
from app.services.score_calculator import calculate_weighted_score


def select_benchmark_node(
    state: BenchmarkState
) -> dict:

    candidate = state["candidate_profile"]

    benchmark = get_existing_benchmark(
        candidate.function
    )

    if benchmark is None:
        return {}

    return {
        "benchmark": benchmark
    }


def generate_benchmark_node(
    state: BenchmarkState
) -> dict:

    candidate = state["candidate_profile"]

    benchmark = generate_benchmark(
        candidate
    )

    return {
        "benchmark": benchmark
    }


def evaluate_candidate_node(
    state: BenchmarkState
) -> dict:

    candidate = state["candidate_profile"]
    benchmark = state["benchmark"]

    candidate_eval = eval_candidate(
        candidate,
        benchmark
    )

    return {
        "evaluation": candidate_eval
    }


def candidate_score_node(
    state: BenchmarkState
) -> dict:

    evaluation = state["evaluation"]
    benchmark = state["benchmark"]

    candidate_score = calculate_weighted_score(
        evaluation,
        benchmark
    )

    return {
        "final_score": candidate_score
    }
def route_benchmark(
    state: BenchmarkState
) -> str:

    if "benchmark" in state:
        return "evaluate"

    return "generate"

