from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

from langgraph.graph import StateGraph,END,START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv
from typing import TypedDict,Annotated

from backend.memory.memory import memory

from backend.tools.web_search import web_search
from backend.tools.rag_tool import rag_tool
import os


load_dotenv()

llm_endpoint = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HF_API_KEY"),
    task="text-generation",
    max_new_tokens=5000,
    temperature=0.7
    
)
llm = ChatHuggingFace(llm=llm_endpoint)

tools = [web_search, rag_tool]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: MessagesState):

    messages = [
        SystemMessage(
            content=(
                """
You are an AI Assistant.

Rules:

1. Use rag_search for uploaded documents.
2. Use web_search for current information.
3. Prefer document information if available.
4. Cite the PDF source when answering.
"""
            )
        )
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


builder = StateGraph(MessagesState)
builder.add_node("chatbot",chatbot)
tool_node = ToolNode(tools)
builder.add_node("tools",tool_node)
builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
builder.add_edge("tools","chatbot")
builder.set_entry_point("chatbot")

print("memory_saver =", memory)
print("type =", type(memory))

graph = builder.compile(
    checkpointer=memory
)
