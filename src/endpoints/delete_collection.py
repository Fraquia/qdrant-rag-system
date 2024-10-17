from fastapi import APIRouter
from src.services.vector_store_services.vector_store_manager import VectorStoreManager

router = APIRouter()


@router.delete("/vector_db/delete_collection")
def delete_collection(collection_name: str):
    vector_store = VectorStoreManager()

    # check collection actually exists
    collections = vector_store.list_collections()
    if not collection_name in collections:
        return {"message": f"{collection_name} does not exists", "status_code": 400}
    else:
        # todo: implement deletion logic
        status = ""
        if status:
            return {"message": f"Collection '{collection_name}' deleted successfully", "status_code": 200}
