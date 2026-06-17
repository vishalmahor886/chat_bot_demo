from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from backend.rag.pdf_loader import load_pdf_data

router = APIRouter()

UPLOAD_DIR="beckend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    try:
        filepath=f"{UPLOAD_DIR}\{file.filename}"

        with open(filepath, 'wb') as buffer:
            buffer.write(await file.read())

        chunk = load_pdf_data(filepath)

        os.remove(filepath)

        return {
            "message": "success",
            "chunks": chunks,
            "file": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

            

