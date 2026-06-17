from langchain.tools import tool
from ddgs import DDGS


@tool
def web_search(query:str)->str:
    """
    You can use this tool to search for information on the internet.
    """
    results =[]
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(
                    f"Title :{r['title']}\nBody :{r['body']}\nHref :{r['href']}"
                )
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Error searching the web: {str(e)}"
    
            

