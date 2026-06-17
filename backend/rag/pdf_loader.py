from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.rag.vector_store import vectorstores

import os

def load_pdf_data(file_path: str, thread_id: str = None):
    loader = PyPDFLoader(file_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(document)

    file_name = os.path.basename(file_path)

    for chunk in chunks:
        chunk.metadata["source"] = file_name
        if thread_id:
            chunk.metadata["thread_id"] = thread_id

    vectorstores.add_documents(chunks)
    return len(chunks), len(document)


