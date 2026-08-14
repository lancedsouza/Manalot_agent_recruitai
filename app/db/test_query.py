from app.db.database import SessionLocal
from app.db.models import Candidate

session = SessionLocal()

candidates = (
    session.query(Candidate)
    .filter(Candidate.experience_years >= 5)
    .all()
)

for candidate in candidates:
    print(candidate.id)
    print(candidate.name)
    print(candidate.experience_years)
    print(candidate.skills)
    print("--------------------")

session.close()