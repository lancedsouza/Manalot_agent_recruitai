from app.db.database import SessionLocal
from app.db.models import Candidate
from app.models.resume import Resume


def save_resume_to_db(
    resume: Resume,
    resume_text: str,
) -> Candidate:
    """
    Save a parsed Pydantic Resume object into PostgreSQL.

    Flow:
        Pydantic Resume
            ↓
        SQLAlchemy Candidate
            ↓
        session.add()
            ↓
        session.commit()
            ↓
        PostgreSQL
    """

    session = SessionLocal()

    try:

        # Convert Pydantic Resume → SQLAlchemy Candidate
        candidate = Candidate(
            name=resume.name,
            experience_years=resume.experience_years,
            skills=resume.skills,
            resume_text=resume_text,
        )

        # Tell SQLAlchemy we want to insert this object
        session.add(candidate)

        # Permanently save to PostgreSQL
        session.commit()

        # Reload DB-generated values such as candidate.id
        session.refresh(candidate)

        print()
        print("Candidate saved to PostgreSQL.")
        print(f"Candidate ID: {candidate.id}")

        return candidate

    except Exception as e:

        # Undo the current transaction if something failed
        session.rollback()

        print()
        print("DATABASE SAVE FAILED")
        print(repr(e))

        raise

    finally:

        # Always release the DB session
        session.close()