import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from qdrant_client.http.models import CollectionsResponse

from src.services.vector_store_services.vector_store_manager import VectorStoreManager


@pytest.fixture
def mock_vector_store():
    with patch.object(VectorStoreManager, "__init__", lambda self: None):
        vs = VectorStoreManager()
        vs.client = MagicMock()
        vs.embeddings = MagicMock()
        # Default: list_collections returns empty
        vs.client.get_collections.return_value = CollectionsResponse(collections=[])
        yield vs


@pytest.fixture
def client(mock_vector_store):
    from src.dependencies import get_vector_store
    from server import create_app

    app = create_app()
    app.dependency_overrides[get_vector_store] = lambda: mock_vector_store

    with TestClient(app) as c:
        yield c
