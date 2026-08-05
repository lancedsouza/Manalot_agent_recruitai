from pydantic import BaseModel
class DecisionEvidence(BaseModel):
    requirement: str
    candidate_evidence: str
    match: bool
    confidence: float