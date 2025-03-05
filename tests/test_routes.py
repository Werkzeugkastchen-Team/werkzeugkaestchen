import pytest
from webapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# So können wir einfach auf Inhalte auf einer Seite prüfen
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tools Hauptseite' in response.data


def test_search_tools(client):
    """Testet die Suchfunktion mit verschiedenen Eingaben"""
    
    response = client.get("/search_tools?q=JSON")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "JSON Validator"

    response = client.get("/search_tools?q=counter")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Word Counter"

    response = client.get("/search_tools?q=base")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Base64 Encoder"

    response = client.get("/search_tools?q=xyz")
    data = response.get_json()
    assert len(data) == 0