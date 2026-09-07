from app.db_jd.db import SessionLocal
from app.db_jd.jd_models import JD
from app.services.embedding_service import create_embedding


def create_and_save_jd(
    designation: str,
    jd_text: str,
):

    if not designation.strip():
        raise ValueError(
            "Designation cannot be empty."
        )

    if not jd_text.strip():
        raise ValueError(
            "JD text cannot be empty."
        )

    # Create ONE embedding for the entire JD
    jd_embedding = create_embedding(
        jd_text
    )

    # Create an instance of the JD model
    jd_record = JD(
        title=designation.strip(),
        description=jd_text,
        embedding=jd_embedding,
    )

    session = SessionLocal()

    try:

        session.add(jd_record)

        session.commit()

        session.refresh(jd_record)

        jd_id = jd_record.chunk_index

        return {
            "id": jd_id,
            "title": jd_record.title,
            "embedding": jd_embedding,
        }

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()