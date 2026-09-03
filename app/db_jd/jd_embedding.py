from pgvector.sqlalchemy import Vector
import requests
from app.db_jd.db import Base
from app.extractors.jd_extractor_new import jd_path,create_chunks

# Create embedding



OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"


def create_embedding() -> list[float]:

    docs=create_chunks(jd_path)
    data_embedded = []

    for i, chunk in enumerate(docs):
        # Create a new JD instance for each chunk
        embedding = requests.post(
            OLLAMA_EMBEDDING_URL,
            json={
                "model": EMBEDDING_MODEL,
                "input": chunk.page_content,
            },
        )

        embedding.raise_for_status()
        embedding = embedding.json()["embeddings"][0]
        data_embedded.append({
            "chunk_index": i,
            "text": chunk.page_content,
            "embedding": embedding
        })
    print(f"Embedded_data: {data_embedded}")
    print(f"Raw_embedding: {embedding}")
    return data_embedded
if __name__ == "__main__":
    # Example usage
    
    embedding = create_embedding() 
    print(f"Embedding: {embedding}")
    
# def create_embedding() -> list[dict]:
#     docs = create_chunks(jd_path)
#     all_embedded_data = []

#     for i, chunk in enumerate(docs):
#         response = requests.post(
#             OLLAMA_EMBEDDING_URL,
#             json={
#                 "model": EMBEDDING_MODEL,
#                 "input": chunk.page_content,  # Sends one chunk at a time
#             },
#         )
#         response.raise_for_status()
        
#         # [0] extracts the vector for THIS current chunk from Ollama's 2D response array
#         vector = response.json()["embeddings"][0]
#         print (f"Vector after embedding{vector}")  # Print the vector for each chunk
        
#         # Save both the chunk text and its vector
#         all_embedded_data.append({
#             "chunk_index": i,
#             "text": chunk.page_content,
#             "embedding": vector
#         })
#         print(f"Successfully embedded chunk {i + 1} of {len(docs)}")
#         print(f"Current embedded data: {all_embedded_data}")  # Print the current state of the list

#     return all_embedded_data

# if __name__ == "__main__":
#     embeddings_list = create_embedding()
#     print(f"Total chunks successfully embedded: {len(embeddings_list)}")
  