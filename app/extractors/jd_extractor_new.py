from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import psycopg2
from pgvector.psycopg2 import register_vector

# Define the target path for the JD file

jd_path = Path(
    "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/test/JD - Sr Manager - Financial Planning & Analytics.docx"
)
def create_chunks(path: Path):
    # Verify if the file is actually present
    if not path.exists():
        print(f"Directory contents of data/: {[f.name for f in path.parent.glob('*') if path.parent.exists()]}")
        raise FileNotFoundError(f"File not found at: {path}")

    loader = Docx2txtLoader(str(path))
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    split_docs = text_splitter.split_documents(docs)
    return split_docs

