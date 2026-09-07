# import requests


# OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embed"
# EMBEDDING_MODEL = "nomic-embed-text"


# def create_embedding(text: str) -> list[float]:

#     response = requests.post(
#         OLLAMA_EMBEDDING_URL,
#         json={
#             "model": EMBEDDING_MODEL,
#             "input": text,
#         },
#     )

#     response.raise_for_status()

#     data = response.json()

#     embedding = data["embeddings"][0]

#     return embedding

# import requests


# OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
# EMBEDDING_MODEL = "nomic-embed-text"


# def create_embedding(text: str) -> list[float]:

#     response = requests.post(
#         OLLAMA_EMBEDDING_URL,
#         json={
#             "model": EMBEDDING_MODEL,
#             "prompt": text,
#         },
#     )

#     response.raise_for_status()

#     data = response.json()

#     embedding = data["embedding"]

#     return embedding

import os

from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def create_embedding(text: str) -> list[float]:

    if not text or not text.strip():
        raise ValueError("Cannot create embedding from empty text")

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768,
        ),
    )

    embedding = response.embeddings[0].values

    return embedding