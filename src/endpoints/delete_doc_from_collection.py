from fastapi import APIRouter
from src.services.vector_store_services.vector_store_manager import VectorStoreManager

router = APIRouter()


@router.delete("/vector_db/delete_doc_from_collection_by_name")
def delete_doc_from_collection(collection_name: str, document_name: str):
    vector_store = VectorStoreManager()

    # check collection actually exists
    collections = vector_store.list_collections()
    if not collection_name in collections:
        return {"message": f"{collection_name} does not exists", "status_code": 400}
    else:
        metadata = {"title": document_name}
        #todo: check UpdateResults type to istantiate status variable
        status = vector_store.delete_docs_by_metadata_filter(
            collection_name=collection_name,
            metadata=metadata,
        )
        if status:
            return {"message": f"Document '{document_name}' deleted successfully from {collection_name}",
                    "status_code": 200}
        else:
            return {"message": f"Failed to delete document '{document_name}' from {collection_name}",
                    "status_code": 400}
