from app.db.database import SessionLocal
from app.db.models import Candidate


session = SessionLocal()


candidate = Candidate(
    name="John Smith",
    experience_years=8.0,
    skills=["Python", "SQL", "PostgreSQL"],
    resume_text="Python developer with 8 years of experience."
)

session.add(candidate)

session.commit()

print("Candidate inserted!")
print("Candidate ID:", candidate.id)

session.close()