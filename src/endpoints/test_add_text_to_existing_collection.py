from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.services.utils.document_utils import create_document
from src.dependencies import get_vector_store

router = APIRouter()


@router.post("/vector_db/add_text_to_existing_collection")
async def add_text_to_existing_collection(collection_name: str, text: dict, vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    doc_list = create_document(text)
    added_status = vector_store.add_documents_to_existing_collection(collection_name, doc_list)

    if added_status is True:
        return {"message": f"Added documents to collection '{collection_name}'"}
    raise HTTPException(status_code=500, detail="Failed to add documents to collection")
