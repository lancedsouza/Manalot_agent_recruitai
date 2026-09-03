from pathlib import Path

from app.services.resume_extractor import (
    extract_resume_data,
    extract_text,
)

from app.services.embedding_service import create_embedding

from app.db.database import SessionLocal
from app.db.models import Candidate


# ============================================================
# RESUME FOLDER
# ============================================================

RESUME_FOLDER = Path(
    "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/test"
)


# ============================================================
# SAVE ONE CANDIDATE
# ============================================================

def save_resume_to_db(
    pdf_path: Path,
):

    session = SessionLocal()

    try:

        print()
        print("=" * 70)
        print(f"Processing: {pdf_path.name}")
        print("=" * 70)

        # ----------------------------------------------------
        # STEP 1
        # PDF -> Pydantic Resume
        # ----------------------------------------------------

        resume = extract_resume_data(
            pdf_path
        )

        print(
            f"Parsed candidate: {resume.name}"
        )


        # ----------------------------------------------------
        # STEP 2
        # PDF -> original full resume text
        # ----------------------------------------------------

        resume_text = extract_text(
            pdf_path
        )


        # ----------------------------------------------------
        # STEP 3
        # Build text that will represent candidate
        # semantically
        # ----------------------------------------------------

        searchable_text = f"""
Candidate: {resume.name}
Experience Years: {resume.experience_years}
Skills: {", ".join(resume.skills)}
"""


        # ----------------------------------------------------
        # STEP 4
        # Text -> embedding
        # ----------------------------------------------------

        embedding = create_embedding(
            searchable_text
        )

        print(
            f"Embedding dimensions: {len(embedding)}"
        )


        # ----------------------------------------------------
        # STEP 5
        # Pydantic Resume -> SQLAlchemy Candidate
        # ----------------------------------------------------

        candidate = Candidate(
            name=resume.name,
            experience_years=resume.experience_years,
            skills=resume.skills,
            resume_text=resume_text,
            embedding=embedding,
        )


        # ----------------------------------------------------
        # STEP 6
        # Save to PostgreSQL
        # ----------------------------------------------------

        session.add(
            candidate
        )

        session.commit()

        session.refresh(
            candidate
        )

        print(
            f"Saved candidate ID: {candidate.id}"
        )


    except Exception as e:

        session.rollback()

        print(
            f"FAILED: {pdf_path.name}"
        )

        print(
            repr(e)
        )


    finally:

        session.close()


# ============================================================
# PROCESS ALL RESUMES
# ============================================================

def save_all_candidates():

    pdf_files = list(
        RESUME_FOLDER.glob("*.pdf")
    )

    print(
        f"Found {len(pdf_files)} resumes."
    )

    for pdf_path in pdf_files:

        save_resume_to_db(
            pdf_path
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    save_all_candidates()