from fastapi import FastAPI

from app.models.candidate_profile import CandidateProfile
from app.agents.benchmark_graph import benchmark_graph


app = FastAPI(
    title="Manalot RecruitAI",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Manalot RecruitAI API is running"
    }


@app.post("/candidates/evaluate")
def evaluate_candidate(
    candidate: CandidateProfile
):

    result = benchmark_graph.invoke(
        {
            "candidate_profile": candidate
        }
    )

    return result