from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector

from app.db_jd.db import Base


class JD(Base):

    __tablename__ = "jds"

    chunk_index = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    embedding = Column(
        Vector(768),
        nullable=False,
    )