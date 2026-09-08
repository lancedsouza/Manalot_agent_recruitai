from sqlalchemy import text

from app.db_jd.db import Base, engine
from app.db_jd.jd_models import JD


def init_db():

    with engine.begin() as connection:
        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )

    Base.metadata.create_all(bind=engine)