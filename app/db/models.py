from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from app.db.database import Base


class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )

    name = Column(
        String,
        nullable=False,
    )

    experience_years = Column(
        Float,
        nullable=False,
    )

    skills = Column(
        ARRAY(String)
    )

    resume_text = Column(
        Text
    )

    embedding = Column(
        Vector(768)
    )