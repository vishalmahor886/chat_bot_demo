from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
load_dotenv()
client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

@tool
def research_tool(topic:str)->str:
    """
    Search the internet and return research results.
    """ 
    results = client.search(
        query=topic,
        search_depth="advanced",
        max_results=5
    )

    answer = ""
    for item in results["results"]:
        answer+=f"""
        Title: {item["title"]}
        Source: {item["url"]}
        Content: {item["content"]}
        --------------------------
        """
    return answer



    
