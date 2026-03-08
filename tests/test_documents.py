from unittest.mock import MagicMock, patch
from qdrant_client.http.models import CollectionsResponse, CollectionDescription


def test_query_collection_not_found(client, mock_vector_store):
    response = client.post("/vector_db/query_collection?collection_name=nonexistent&query=test&k=3")
    assert response.status_code == 404


def test_query_collection_success(client, mock_vector_store):
    mock_vector_store.client.get_collections.return_value = CollectionsResponse(
        collections=[CollectionDescription(name="test_col")]
    )

    mock_doc = MagicMock()
    mock_doc.page_content = "Sample content"

    with patch.object(mock_vector_store, "load_collection") as mock_load:
        mock_collection = MagicMock()
        mock_collection.similarity_search.return_value = [mock_doc]
        mock_load.return_value = mock_collection

        with patch.object(mock_vector_store, "retrieve_documents_from_collection", return_value=["Sample content"]):
            response = client.post("/vector_db/query_collection?collection_name=test_col&query=test&k=3")
            assert response.status_code == 200


def test_delete_doc_not_found_collection(client, mock_vector_store):
    response = client.delete("/vector_db/delete_doc_from_collection_by_name?collection_name=nonexistent&document_name=doc1")
    assert response.status_code == 404


def test_add_text_not_found_collection(client, mock_vector_store):
    response = client.post(
        "/vector_db/add_text_to_existing_collection?collection_name=nonexistent",
        json={"item1": {"descrizione": "test", "nome": "test_doc"}}
    )
    assert response.status_code == 404
