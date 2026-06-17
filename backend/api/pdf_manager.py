from fastapi import APIRouter, HTTPException
from backend.rag.vector_store import vectorstores

router = APIRouter()

@router.get("/list-pdfs")
def list_pdfs(thread_id: str = None):
    try:
        where_clause = {"thread_id": thread_id} if thread_id else None
        
        if where_clause:
            results = vectorstores._collection.get(where=where_clause)
        else:
            results = vectorstores._collection.get()
        
        sources = set()
        for metadata in results.get("metadatas", []):
            if metadata and "source" in metadata:
                sources.add(metadata["source"])
                
        return {"pdfs": list(sources)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-pdf/{filename}")
def delete_pdf(filename: str, thread_id: str = None):
    try:
        where_clause = {"source": filename}
        if thread_id:
            where_clause["thread_id"] = thread_id
            
        vectorstores._collection.delete(where=where_clause)
        return {"message": f"Deleted {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
