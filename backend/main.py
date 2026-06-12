from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from  pydantic import BaseModel
from backend.chain import get_chat_chain
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# ✅ CORS (REQUIRED for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chain = get_chat_chain()

class ChatRequest(BaseModel):
    message:str

def generate_stream(message:str):
    for chunk in chain.stream({"input": message}):
        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content

@app.post("/chat")
async def chat(request: ChatRequest):
    return StreamingResponse(
        content=generate_stream(request.message),
        media_type="text/plain"
    )
