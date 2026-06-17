from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from backend.rag.pdf_loader import load_pdf_data

router = APIRouter()

UPLOAD_DIR="backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-pdf")
async def upload_file(thread_id: str = None, file: UploadFile = File(...)):
    try:
        filepath = os.path.join(UPLOAD_DIR, file.filename)

        with open(filepath, 'wb') as buffer:
            buffer.write(await file.read())

        chunks_count, pages_count = load_pdf_data(filepath, thread_id)

        os.remove(filepath)

        return {
            "message": "success",
            "chunks": chunks_count,
            "pages": pages_count,
            "file": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

            

