from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.graph.graph_builder import graph
from backend.api.chat import router as chat_router
from backend.api.upload import router as upload_router
from backend.api.pdf_manager import router as pdf_manager_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def home():
    return {"status": "running"}

app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(pdf_manager_router)

