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
