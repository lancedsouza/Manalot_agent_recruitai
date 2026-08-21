from pydantic import BaseModel, Field


class EvaluationCriterion(BaseModel):
    name: str
    description: str


class BenchmarkDimension(BaseModel):
    name: str
    description: str
    weight: float

    evaluation_criteria: list[EvaluationCriterion] = Field(
        default_factory=list
    )


class RoleBenchmark(BaseModel):
    function: str
    dimensions: list[BenchmarkDimension]