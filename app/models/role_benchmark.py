from pydantic import BaseModel


class BenchmarkDimension(BaseModel):
    name: str
    description: str
    weight: float


class RoleBenchmark(BaseModel):
    function: str
    dimensions: list[BenchmarkDimension]