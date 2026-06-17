from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from backend.graph.graph_builder import graph

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    thread_id: str


def generate_stream(message: str, thread_id: str):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    for event in graph.stream(
        {"messages": [("human", message)]},
        config=config
    ):
        if "chatbot" in event:
            msg = event["chatbot"]["messages"][-1]

            if hasattr(msg, "content") and msg.content:
                yield msg.content


@router.post("/chat")
def chat(request: ChatRequest):

    return StreamingResponse(
        generate_stream(request.message, request.thread_id),
        media_type="text/plain"
    )