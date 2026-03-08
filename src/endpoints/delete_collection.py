from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store

router = APIRouter()


@router.delete("/vector_db/delete_collection")
def delete_collection(collection_name: str, vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    status = vector_store.delete_collection(collection_name)
    if status:
        return {"message": f"Collection '{collection_name}' deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete collection")
