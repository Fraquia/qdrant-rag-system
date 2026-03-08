from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store

router = APIRouter()


@router.get("/vector_db/get_collection_info")
def get_collection_info(collection_name: str, vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    documents = vector_store.get_all_docs_from_collection(collection_name=collection_name)
    if documents:
        return {"documents": documents}
    raise HTTPException(status_code=404, detail=f"No documents found in '{collection_name}'")
