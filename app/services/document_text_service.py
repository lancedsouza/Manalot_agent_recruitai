import os
import tempfile
from pathlib import Path

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
)


def extract_uploaded_document(uploaded_file) -> str:
    """
    Extract full text from a Streamlit UploadedFile.

    Supported formats:
    - PDF
    - DOCX
    """

    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix not in [".pdf", ".docx"]:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = temp_file.name

        if suffix == ".pdf":

            loader = PyPDFLoader(
                temp_path
            )

        elif suffix == ".docx":

            loader = Docx2txtLoader(
                temp_path
            )

        docs = loader.load()

        full_text = "\n".join(
            doc.page_content
            for doc in docs
            if doc.page_content
        )

        return full_text.strip()

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)