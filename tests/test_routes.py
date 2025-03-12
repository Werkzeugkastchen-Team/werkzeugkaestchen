import pytest
from webapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# So können wir einfach auf Inhalte auf einer Seite prüfen
def test_index_route(client):
    """Testet, ob die Hauptseite den Titel mit Werkzeug- beinhaltet"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Werkzeug' in response.data


def test_search_tools(client):
    """Testet die Suchfunktion mit verschiedenen Eingaben"""
    
    response = client.get("/search_tools?q=Dateigrößenberechner")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Dateigrößenberechner"

    response = client.get("/search_tools?q=Bildkonverter")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Bildkonverter"

    # this might fail when fuzzy search matches xyz
    response = client.get("/search_tools?q=xyz")
    data = response.get_json()
    assert len(data) == 0