from fastapi import APIRouter
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.services.utils.document_utils import create_document

router = APIRouter()


@router.get("/vector_db/list_all_collections")
async def list_al_collections():
    try:
        vector_store = VectorStoreManager()
        collections_list = vector_store.list_collections()
        return {"message": "Operation successful",
                "response": [{"collections_list": collections_list}],
                "status_code": 200}

    except Exception as e:
        return {"message": f"Failed to retrieve collections for {str(e)}", "status_code": 400}
