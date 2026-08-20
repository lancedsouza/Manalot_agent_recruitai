from app.db.database import SessionLocal
from app.db.models import Candidate
from app.services.embedding_service import create_embedding


query = """
Senior FP&A leader with forecasting,
financial modeling and automation experience
"""


query_embedding = create_embedding(query)

print("Query:")
print(query)

print()
print("Embedding dimensions:", len(query_embedding))


session = SessionLocal()

try:

    results = (
        session.query(
            Candidate,
            Candidate.embedding.cosine_distance(
                query_embedding
            ).label("distance")
        )
        .filter(
            Candidate.embedding.isnot(None)
        )
        .order_by(
            Candidate.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(5)
        .all()
    )


    print()
    print("=" * 70)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 70)


    for candidate, distance in results:

        similarity = 1 - distance

        print()
        print("Name:", candidate.name)
        print(
            "Experience:",
            candidate.experience_years
        )
        print(
            "Similarity:",
            round(similarity, 4)
        )
        print(
            "Skills:",
            candidate.skills
        )

        print("-" * 70)


finally:

    session.close()