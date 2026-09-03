from app.db_jd.db import SessionLocal
from app.db_jd.jd_models import JD
from app.db.models import Candidate
from app.utils.similarity import similarity
from statistics import mean as average


def match_candidates_with_jd(min_experience=0):

    session = SessionLocal()

    jd_parts = session.query(JD).all()

    candidates = (
        session.query(Candidate)
        .filter(Candidate.experience_years >= min_experience)
        .all()
    )

    results = []

    for candidate in candidates:

        scores = []

        for jd_part in jd_parts:

            score = similarity(
                jd_part.embedding,
                candidate.embedding
            )

            scores.append(score)

        overall_score = average(scores)

        results.append({
            "Candidate": candidate.name,
            "Experience": candidate.experience_years,
            "Similarity": round(overall_score, 4)
        })

    session.close()

    return results