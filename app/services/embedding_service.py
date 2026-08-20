import requests


OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"


def create_embedding(text: str) -> list[float]:

    response = requests.post(
        OLLAMA_EMBEDDING_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": text,
        },
    )

    response.raise_for_status()

    data = response.json()

    embedding = data["embeddings"][0]

    return embedding