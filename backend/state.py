from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
class State(TypedDict):
    message: Annotated[list, add_messages]
    