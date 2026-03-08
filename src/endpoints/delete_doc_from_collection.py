from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store

router = APIRouter()


@router.delete("/vector_db/delete_doc_from_collection_by_name")
def delete_doc_from_collection(collection_name: str, document_name: str, vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    metadata = {"title": document_name}
    status = vector_store.delete_docs_by_metadata_filter(
        collection_name=collection_name,
        metadata=metadata,
    )
    if status:
        return {"message": f"Document '{document_name}' deleted from '{collection_name}'"}
    raise HTTPException(status_code=500, detail=f"Failed to delete document '{document_name}'")
