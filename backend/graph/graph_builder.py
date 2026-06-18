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
from backend.tools.coding_tool import coding_agent
from backend.agents.email_sender_agent import email_sender
from backend.agents.research_agent import research_tool_agent
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

tools = [web_search, rag_tool, coding_agent, email_sender, research_tool_agent ]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: MessagesState):

    messages = [
        SystemMessage(
            content=(
                """

You are a Multi Agent AI Assistant.

Available Agents:
1. coding_tool
    - write code
    - debug code
    - explain code

2. rag_tool
    - search inside pdfs
    - answer questions based on pdfs

3. web_search
    - search on internet
    - answer questions based on internet

4. Email Sender Tool
    - When user asks to send an email,
    extract:
        - recipient email
        - subject
        - body
5. Research Tool
    -latest news
    - current events
    - internet research
    - company information
    - comparisons
    - market trends

and call email_sender.

Rules:
1. Choose the tool that best suits the user's query.
2. If the query is about coding, use coding_tool.
3. If the query is about pdfs or Documents, use rag_tool.
4. If the query is about internet, use web_search.
5. If the query is about send email, use email_sender.
6. If the query is about research, use research_tool_agent.
7. If the query is about multiple things, use the tool that best suits the user's query.
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
