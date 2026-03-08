def test_query_request_invalid_k_too_high(client):
    response = client.post(
        "/chat/chat_agent",
        json={"query": "test", "collection_name": "test_col", "k": 200}
    )
    assert response.status_code == 422


def test_query_request_invalid_k_zero(client):
    response = client.post(
        "/chat/chat_agent",
        json={"query": "test", "collection_name": "test_col", "k": 0}
    )
    assert response.status_code == 422


def test_query_request_invalid_collection_name(client):
    response = client.post(
        "/chat/chat_agent",
        json={"query": "test", "collection_name": "invalid name!", "k": 5}
    )
    assert response.status_code == 422


def test_query_request_empty_query(client):
    response = client.post(
        "/chat/chat_agent",
        json={"query": "", "collection_name": "test_col", "k": 5}
    )
    assert response.status_code == 422
