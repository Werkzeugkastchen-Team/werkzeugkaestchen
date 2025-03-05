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
    assert b'Digitale Werkzeuge' in response.data


def test_search_tools(client):
    """Testet die Suchfunktion mit verschiedenen Eingaben"""
    
    response = client.get("/search_tools?q=JSON")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "JSON Validation Tool"

    response = client.get("/search_tools?q=word")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Word Counting Tool"

    # this might fail when fuzzy search matches xyz
    response = client.get("/search_tools?q=xyz")
    data = response.get_json()
    assert len(data) == 0