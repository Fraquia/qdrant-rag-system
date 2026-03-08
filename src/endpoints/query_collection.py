from fastapi import APIRouter, Depends, HTTPException
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store

router = APIRouter()


@router.post("/vector_db/query_collection")
def query_collection(collection_name: str, query: str, k: int, vector_store: VectorStoreManager = Depends(get_vector_store)):
    collections = vector_store.list_collections()
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    documents = vector_store.retrieve_documents_from_collection(
        collection_name=collection_name,
        query=query,
        k=k
    )
    if documents:
        return {"documents": documents}
    raise HTTPException(status_code=404, detail=f"No results found in '{collection_name}'")
