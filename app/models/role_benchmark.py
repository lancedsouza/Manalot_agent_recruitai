from pydantic import BaseModel
class EvalutionCriteriria(BaseModel):
    name:str
    description:str

class BenchmarkDimension(BaseModel):
    name: str
    description: str
    weight: float
    evaluation_criteria:list[EvalutionCriteriria]


class RoleBenchmark(BaseModel):
    function: str
    dimensions: list[BenchmarkDimension]