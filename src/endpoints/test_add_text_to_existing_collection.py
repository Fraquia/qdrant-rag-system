from fastapi import APIRouter, UploadFile, File
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.services.utils.document_utils import create_document

router = APIRouter()


@router.post("/vector_db/add_text_to_existing_collection")
async def add_text_to_existing_collection(collection_name: str, text: dict):
    vector_store = VectorStoreManager()

    # check collection actually exists
    collections = vector_store.list_collections()
    if not collection_name in collections:
        return {"error": f"Collection '{collection_name}' does not exist"}
    else:
        doc_list = create_document(text)
        added_status = vector_store.add_documents_to_existing_collection(collection_name, doc_list)

        if added_status:
            return {"message": f"Added documents to collection '{collection_name}", "status_code": 200}
        else:
            return {"message": f"Failed to add documents to collection '{collection_name}",  "status_code": 400}