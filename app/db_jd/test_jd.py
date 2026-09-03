from app.db_jd.db import SessionLocal 
from app.db_jd.jd_models import JD


session = SessionLocal()

def load_jd_chunks():
    jd_chunks = (
        session.query(JD)
        .order_by(JD.chunk_index)
        .all()
    )

    return jd_chunks

if __name__ == "__main__":
    chunks = load_jd_chunks()
    print(f"Loaded {len(chunks)} JD chunks from the database.")
    print("First chunk details:")
    print(f"Chunks : {chunks}")
    print(type(chunks))
    for i in chunks:
        print(f"Chunk Index: {i.chunk_index}")
        print(f"Title: {i.title}")
        print(f"Description: {i.description}")
        print(f"Embedding: {i.embedding}")
        print("--------------------")