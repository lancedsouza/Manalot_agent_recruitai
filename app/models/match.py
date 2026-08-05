from pydantic import BaseModel

class MatchResult(BaseModel):
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    experience_gap: float
    explanation: str