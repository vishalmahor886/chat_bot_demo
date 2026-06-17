from langchain.tools import tool
from backend.rag.retrivever import retrivever

@tool
def rag_tool(query:str)->str:
    """
        Search Uploaded PDF Documents
    """

    docs = retrivever.invoke(query)

    if not docs:
            return "No relevent information found"
    context = []

    for doc in docs:
        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        context.append(
            f"[Source:{source}]\n{doc.page_content}"
        )

    return "\n\n".join(context)