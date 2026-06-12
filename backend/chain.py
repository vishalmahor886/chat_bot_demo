import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

from langgraph.graph import StateGraph,END,START
from langgraph.prebuilt import ToolNode, tools_condition


load_dotenv()

def get_chat_chain():
    llm = ChatGroq(
        api_key= os.getenv("GROQ_API_KEY"), 
        model_name = "llama-3.3-70b-versatile"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        ("human", "{input}")
    ])

    chain = prompt | llm
    return chain
