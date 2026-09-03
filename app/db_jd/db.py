import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

url = os.getenv("DATABASE_URL") 
if not url:
    raise ValueError("DATABASE_URL not found in .env")  

engine = create_engine(
    url,
    echo=True
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    # Example usage: Create a new session and print the engine URL
    session = SessionLocal()
    print(f"Connected to database at: {engine.url}")
    session.close()
