from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.dialects.postgresql import ARRAY        
from pgvector.sqlalchemy import Vector
from app.db_jd.db import Base


class JD(Base):

    __tablename__ = "jds"

    chunk_index = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    title = Column(
        String,
        nullable=False,
        default="Sr. Manager-FP&A",
    )

    description = Column(
        Text,
        nullable=False,
    )

    

    embedding = Column(
        Vector(768),
        nullable=False,
    )