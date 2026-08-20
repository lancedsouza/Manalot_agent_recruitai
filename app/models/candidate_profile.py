from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    # From UI
    name: str
    designation: str
    function: str
    industry: str
    experience_years: float
    geography: str

    # Leadership / scope
    team_size: int | None = None
    largest_team_size: int | None = None

    # Scale
    markets: str = ""
    portfolio_handled: str = ""
    budget_handled: str = ""

    # Impact
    business_impact: str = ""
    transformation_scope: str = ""

    # From resume extraction
    skills: list[str] = Field(default_factory=list)
    experience_summary: str = ""
    education_summary: str = ""