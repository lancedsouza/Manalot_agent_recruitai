from app.db.database import SessionLocal
from app.db.models import Candidate
from app.models.resume import Resume
from app.services.embedding_service import create_embedding


def save_resume_to_db(
    resume: Resume,
    resume_text: str,
) -> Candidate:

    session = SessionLocal()

    try:

        # ----------------------------------------------------
        # STEP 1 — Build text for semantic search
        # ----------------------------------------------------

        searchable_text = f"""
Candidate: {resume.name}
Experience Years: {resume.experience_years}
Skills: {", ".join(resume.skills)}
"""

        # ----------------------------------------------------
        # STEP 2 — Convert text → 768-dim embedding
        # ----------------------------------------------------

        embedding = create_embedding(searchable_text)

        # ----------------------------------------------------
        # STEP 3 — Convert Pydantic Resume → SQLAlchemy Candidate
        # ----------------------------------------------------

        candidate = Candidate(
            name=resume.name,
            experience_years=resume.experience_years,
            skills=resume.skills,
            resume_text=resume_text,
            embedding=embedding,
        )

        # ----------------------------------------------------
        # STEP 4 — Save candidate
        # ----------------------------------------------------

        session.add(candidate)

        session.commit()

        session.refresh(candidate)

        print()
        print("Candidate saved to PostgreSQL.")
        print(f"Candidate ID: {candidate.id}")
        print(f"Embedding dimensions: {len(embedding)}")

        return candidate

    except Exception as e:

        session.rollback()

        print()
        print("DATABASE SAVE FAILED")
        print(repr(e))

        raise

    finally:

        session.close()