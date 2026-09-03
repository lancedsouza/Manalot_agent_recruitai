# from app.db_jd.jd_models import JD
# from app.db_jd.db import SessionLocal
# from app.extractors.jd_extractor_new import jd_path
# from app.db_jd.jd_embedding import create_embedding


# def save_jd_to_db():
#     # Create a new database session
#     session = SessionLocal()
    

#     try:
        

#         # Create embeddings for the chunks
#         embedded_data = create_embedding()

#         # Save each chunk and its embedding to the database
#         for i in embedded_data:
#             jd_entry = JD(
#                 chunk_index=i["chunk_index"],
#                 description=i["text"],
#                 embedding=i["embedding"]
#             )
#             session.add(jd_entry)

#         # Commit the transaction
#         session.commit()
#         print("JD chunks and embeddings saved to the database successfully.")

#     except Exception as e:
#         session.rollback()
#         print(f"An error occurred: {e}")

#     finally:
#         session.close()


# if __name__ == "__main__":
#     save_jd_to_db()
from app.db_jd.jd_models import JD
from app.db_jd.db import SessionLocal, engine, Base  # <-- Import engine and Base
from app.extractors.jd_extractor_new import jd_path
from app.db_jd.jd_embedding import create_embedding


def save_jd_to_db():
    # 1. Automatically create tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

    # 2. Create database session
    session = SessionLocal()

    try:
        embedded_data = create_embedding()

        for i in embedded_data:
            jd_entry = JD(
                chunk_index=i["chunk_index"],
                description=i["text"],
                embedding=i["embedding"]
            )
            session.add(jd_entry)

        session.commit()
        print("JD chunks and embeddings saved to the database successfully.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    save_jd_to_db()