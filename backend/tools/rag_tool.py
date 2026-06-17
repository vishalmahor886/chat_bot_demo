from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from backend.rag.vector_store import vectorstores

@tool
def rag_tool(query: str, config: RunnableConfig) -> str:
    """
        Search Uploaded PDF Documents
    """
    thread_id = config.get("configurable", {}).get("thread_id")
    search_kwargs = {"k": 4}
    
    if thread_id:
        search_kwargs["filter"] = {"thread_id": thread_id}
        
    retriever = vectorstores.as_retriever(search_kwargs=search_kwargs)
    docs = retriever.invoke(query)

    if not docs:
        return "No relevent information found"
    context = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        context.append(f"[Source:{source}]\n{doc.page_content}")

    return "\n\n".join(context)