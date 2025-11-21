from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_read_main():
    # Test that the app loads (health check implicit)
    # We don't have a root endpoint, but we can check docs
    response = client.get("/docs")
    assert response.status_code == 200

def test_query_endpoint_validation():
    # Test missing field
    response = client.post("/query", json={})
    assert response.status_code == 422

# We mock the graph execution to avoid calling actual LLMs during tests
# This requires more complex mocking, so for now we stick to basic API structure tests.
