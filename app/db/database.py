from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = (
    "postgresql+psycopg2://"
    "recruitai:recruitai_password"
    "@localhost:5431/recruitai"
)
engine = create_engine(
    DATABASE_URL,
    echo=True  # ← Logs all SQL queries
)
SessionLocal = sessionmaker(
    bind=engine,        # Use this engine
    autoflush=False,    # Don't auto-flush
    autocommit=False    # Don't auto-commit (use transactions)
)