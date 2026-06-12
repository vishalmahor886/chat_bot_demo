from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from backend.graph import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    thread_id: str


@app.get("/")
def home():
    return {"status": "running"}

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


@app.post("/chat")
def chat(request: ChatRequest):

    return StreamingResponse(
        generate_stream(request.message, request.thread_id),
        media_type="text/plain"
    )