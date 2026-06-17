from langchain_community.vectorstores import Chroma
from backend.rag.embeddings import embeddings

VECTOR_DB = "backend/chroma_db"

vectorstores = Chroma(
    persist_directory=VECTOR_DB,
    embedding_function=embeddings
)

