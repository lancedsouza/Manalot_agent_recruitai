from app.db_jd.db import SessionLocal
from app.db.models import Candidate
from app.utils.similarity import similarity


def match_candidates_with_jd(jd_embedding, min_experience=0):

    session = SessionLocal()

    try:
        candidates = (
            session.query(Candidate)
            .filter(Candidate.experience_years >= min_experience)
            .all()
        )

        results = []

        for candidate in candidates:

            if candidate.embedding is None:
                continue

            score = similarity(
                jd_embedding,
                candidate.embedding
            )

            results.append({
                "Candidate": candidate.name,
                "Experience": candidate.experience_years,
                "Match Score": round(score, 4)
            })

        results.sort(
            key=lambda x: x["Match Score"],
            reverse=True
        )

        return results

    finally:
        session.close()