from fastapi import APIRouter
from src.services.vector_store_services.vector_store_manager import VectorStoreManager

router = APIRouter()


@router.get("/vector_db/get_collection_info")
def get_collection_info(collection_name: str):
    vector_store = VectorStoreManager()

    # check collection actually exists
    collections = vector_store.list_collections()
    if not collection_name in collections:
        return {"message": f"{collection_name} does not exists", "status_code": 400}
    else:
        documents = vector_store.get_all_docs_from_collection(
            collection_name=collection_name
        )
        if documents:
            return {"message": "Operation successful",
                    "response": [{"documents_list": documents}],
                    "status_code": 200}
        else:
            return {"message": f"Failed to retrieve documents from {collection_name}",
                    "status_code": 400}
