from functools import lru_cache
from src.services.vector_store_services.vector_store_manager import VectorStoreManager


@lru_cache()
def get_vector_store() -> VectorStoreManager:
    return VectorStoreManager()
