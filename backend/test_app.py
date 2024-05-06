# test_app.py

import pytest
from flask import json
from app import app as flask_app  # Import your Flask app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_analyze_review(client):
    # Send a POST request with JSON data and test the response
    response = client.post('/analyze', json={"review": "This product is good"})
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'success'
    assert 'data' in json.loads(response.data)
