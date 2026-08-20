from pydantic import BaseModel, Field


class DimensionScore(BaseModel):
    dimension: str

    score: float = Field(
        ge=0,
        le=10
    )

    evidence: list[str] = Field(
        default_factory=list
    )

    analysis: str


class BenchmarkEvaluation(BaseModel):
    function: str

    dimension_scores: list[DimensionScore]

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    improvements: list[str] = Field(
        default_factory=list
    )

    overall_analysis: str