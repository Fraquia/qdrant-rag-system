from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store

router = APIRouter()


@router.post("/vector_db/create_collection")
def create_collection(collection_name: str, vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name in collections:
        raise HTTPException(status_code=400, detail=f"Collection '{collection_name}' already exists")

    status = vector_store.create_collection(collection_name)
    if status:
        return {"message": f"Collection '{collection_name}' created successfully"}
    raise HTTPException(status_code=500, detail="Failed to create collection")
