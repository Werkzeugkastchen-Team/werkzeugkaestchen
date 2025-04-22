import pytest
from bs4 import BeautifulSoup
from webapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with client.session_transaction() as session:
            session.clear()
        yield client

def test_german_language_switch(client):
    response = client.get('/?language=de', follow_redirects=True)
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.data, 'html.parser')
    contact_link = soup.find('a', string='Kontakt')
    about_link = soup.find('a', string='Über uns')
    
    assert contact_link is not None
    assert about_link is not None
    assert 'Werkzeugkästchen' in response.text

def test_english_language_switch(client):
    response = client.get('/?language=en', follow_redirects=True)
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.data, 'html.parser')
    contact_link = soup.find('a', string='Contact')
    about_link = soup.find('a', string='About us')
    
    assert contact_link is not None
    assert about_link is not None
    assert 'ToolTiles' in response.text
