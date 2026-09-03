from statistics import mean
from app.db_jd.db import SessionLocal
from app.db_jd.jd_models import JD
from app.db.models import Candidate
from app.utils.similarity import similarity


def match_candidates_with_jd(min_experience=0):

    session = SessionLocal()

    try:
        jd_parts = session.query(JD).all()

        candidates = (
            session.query(Candidate)
            .filter(Candidate.experience_years >= min_experience)
            .all()
        )

        results = []

        for candidate in candidates:

            if candidate.embedding is None:
                continue

            scores = []

            for jd_part in jd_parts:
                score = similarity(
                    jd_part.embedding,
                    candidate.embedding
                )
                scores.append(score)

            if scores:
                overall_score = mean(scores)

                results.append({
                    "Candidate": candidate.name,
                    "Experience": candidate.experience_years,
                    "Match Score": round(overall_score, 4)
                })

        results.sort(
            key=lambda x: x["Match Score"],
            reverse=True
        )

        return results

    finally:
        session.close()