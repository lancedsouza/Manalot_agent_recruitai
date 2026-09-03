from app.db_jd.db import SessionLocal
from app.db_jd.jd_models import JD
from app.db.models import Candidate
from app.utils.similarity import similarity
from statistics import mean as average

session = SessionLocal()

jd_parts = session.query(JD).all()

candidates = (
    session.query(Candidate)
    .filter(Candidate.experience_years >= 5)
    .all()
)

for candidate in candidates:

    scores = []

    for jd_part in jd_parts:

        score = similarity(
            jd_part.embedding,
            candidate.embedding
        )

        scores.append(score)

    overall_score = average(scores)

    print(candidate.name, overall_score)