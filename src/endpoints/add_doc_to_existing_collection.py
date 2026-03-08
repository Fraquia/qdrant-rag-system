import tempfile
import os

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.services.document_manager.document_loader import FileHandler
from src.dependencies import get_vector_store

router = APIRouter()


@router.post("/vector_db/add_doc_to_existing_collection")
def add_doc_to_existing_collection(collection_name: str, file: UploadFile = File(...), vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    tmp_path = None
    try:
        contents = file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        file_handler = FileHandler()
        documents = file_handler.load_pdf(tmp_path, source=file.filename)

        if not documents:
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

        added_status = vector_store.add_documents_to_existing_collection(collection_name, documents)
        if added_status is True:
            return {"message": f"Added {len(documents)} chunks from '{file.filename}' to '{collection_name}'"}
        raise HTTPException(status_code=500, detail="Failed to add documents to collection")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
