from pydantic import BaseModel

class JobDescription(BaseModel):
    title: str
    required_skills: list[str]
    experience_required: float
    domain: str
    responsibilities: list[str]