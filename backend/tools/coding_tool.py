from langchain_core.tools import tool

@tool
def coding_agent(query:str)->str:
    """
    Use this tool for 
    - writing code 
    - debugging code
    - explaining code

    """

    return f"""Coding Request:
        {query}


        Generate code and explaination 
        
        """