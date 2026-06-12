import os
import langchain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

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
