from fastapi import APIRouter
from src.services.vector_store_services.vector_store_manager import VectorStoreManager

router = APIRouter()


@router.post("/vector_db/create_collection")
def create_collection(collection_name: str):
    vector_store = VectorStoreManager()

    # check collection actually exists
    collections = vector_store.list_collections()
    if collection_name in collections:
        return {"message": f"{collection_name} already exists", "status_code": 400}
    else:
        status = vector_store.create_collection(collection_name)
        if status:
            return {"message": f"Collection '{collection_name}' created successfully", "status_code": 200}
