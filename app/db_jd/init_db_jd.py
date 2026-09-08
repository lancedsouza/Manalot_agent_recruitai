from app.db_jd.db import Base, engine

# Import models so SQLAlchemy knows about them
from app.db_jd.jd_models import JD


def init_db():
    Base.metadata.create_all(bind=engine)