from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

from langgraph.graph import StateGraph,END,START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv
from typing import TypedDict,Annotated

from backend.memory import memory
from backend.tool import web_search
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

tools = [web_search]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: MessagesState):

    messages = [
        SystemMessage(
            content=(
                "You are a helpful AI assistant. "
                "Use web_search whenever current or live information is needed."
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
graph = builder.compile(
    checkpointer=memory
)
