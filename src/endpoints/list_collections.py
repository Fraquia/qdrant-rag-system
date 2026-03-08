from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store
import logging

router = APIRouter()


@router.get("/vector_db/list_all_collections")
def list_all_collections(vector_store: VectorStoreManager = Depends(get_vector_store)):
    try:
        collections_list = vector_store.list_collections()
        return {"collections": collections_list}
    except Exception as e:
        logging.error(f"Failed to retrieve collections: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve collections")
