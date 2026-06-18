from backend.tools.research_tool import research_tool
from langchain_core.tools import tool

@tool
def research_tool_agent(topic:str)->str:
    """
    use this tool to search for information for research on the internet and return the results
    """
    try:
        return research_tool.invoke(topic)
    except Exception as e:
        return f"Error researching: {str(e)}"