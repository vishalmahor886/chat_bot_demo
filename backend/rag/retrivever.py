from backend.rag.vector_store import vectorstores

retrivever = vectorstores.as_retriever(
    search_kwargs={"k": 4}
)