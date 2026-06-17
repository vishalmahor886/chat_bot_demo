from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.rag.vector_store import vectorstores

def load_pdf_data(file_path:str):
    loader = PyPDFLoader(file_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(document)

    file_name = file_path.split("/")[-1]

    for chunk in chunks:
        chunk.metadata["source"] = file_name

    vectorstores.add_documents(chunks)
    return len(chunks)


