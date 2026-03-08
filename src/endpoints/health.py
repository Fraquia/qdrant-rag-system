from fastapi import APIRouter, Depends
from src.services.vector_store_services.vector_store_manager import VectorStoreManager
from src.dependencies import get_vector_store
from src.definitions.responses.health.health_200_ok import HealthResponse200Ok
from src.definitions.responses.health.non_health import NonHealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse200Ok | NonHealthResponse)
def health_check(vector_store: VectorStoreManager = Depends(get_vector_store)):
    try:
        vector_store.client.get_collections()
        return HealthResponse200Ok(status=200, description="Up and running")
    except Exception:
        return NonHealthResponse(status=503, description="Qdrant is not reachable")
