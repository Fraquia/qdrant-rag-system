from qdrant_client.http.models import CollectionsResponse, CollectionDescription


def test_create_collection_success(client, mock_vector_store):
    mock_vector_store.client.create_collection.return_value = True
    response = client.post("/vector_db/create_collection?collection_name=test_col")
    assert response.status_code == 200
    assert "created successfully" in response.json()["message"]


def test_create_collection_already_exists(client, mock_vector_store):
    mock_vector_store.client.get_collections.return_value = CollectionsResponse(
        collections=[CollectionDescription(name="test_col")]
    )
    response = client.post("/vector_db/create_collection?collection_name=test_col")
    assert response.status_code == 400


def test_delete_collection_not_found(client, mock_vector_store):
    response = client.delete("/vector_db/delete_collection?collection_name=nonexistent")
    assert response.status_code == 404


def test_delete_collection_success(client, mock_vector_store):
    mock_vector_store.client.get_collections.return_value = CollectionsResponse(
        collections=[CollectionDescription(name="test_col")]
    )
    mock_vector_store.client.delete_collection.return_value = True
    response = client.delete("/vector_db/delete_collection?collection_name=test_col")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]


def test_list_collections(client, mock_vector_store):
    mock_vector_store.client.get_collections.return_value = CollectionsResponse(
        collections=[CollectionDescription(name="col1"), CollectionDescription(name="col2")]
    )
    response = client.get("/vector_db/list_all_collections")
    assert response.status_code == 200


def test_health_check_success(client, mock_vector_store):
    mock_vector_store.client.get_collections.return_value = CollectionsResponse(collections=[])
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_health_check_failure(client, mock_vector_store):
    mock_vector_store.client.get_collections.side_effect = Exception("Connection refused")
    response = client.get("/health")
    assert response.json()["status"] == 503
