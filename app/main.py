from models.resume import Resume
from models.job import JobDescription
from models.match import MatchResult


resume = Resume(
    name="Test Candidate",
    skills=["Python", "Docker"],
    experience_years=5,
    education=["B.Tech"],
    projects=["AI chatbot"],
    companies=["ABC Ltd"]
)


job = JobDescription(
    title="Senior Manager AI",
    required_skills=["Python", "Leadership"],
    preferred_skills=["Docker"],
    experience_required=7,
    domain="Technology",
    responsibilities=["Lead AI team"]
)


result = MatchResult(
    score=75,
    matched_skills=["Python"],
    missing_skills=["Leadership"],
    experience_gap=2,
    explanation="Strong technical match but lacks leadership experience"
)


print(resume)
print(job)
print(result)