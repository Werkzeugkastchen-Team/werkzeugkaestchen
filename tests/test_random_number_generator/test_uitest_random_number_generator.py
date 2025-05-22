import pytest
from bs4 import BeautifulSoup
from webapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_random_number_generator_ui_form(client):
    """Test if the random number generator form loads correctly"""
    response = client.get('/tool/RandomNumberGeneratorTool')
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.data, 'html.parser')

    assert "Zufallszahlengenerator" in soup.title.string
    
    min_input = soup.find('input', {'name': 'Kleinste Zahl'})
    max_input = soup.find('input', {'name': 'Größte Zahl'})
    rolls_input = soup.find('input', {'name': 'Anzahl der Würfe'})
    
    assert min_input is not None
    assert max_input is not None
    assert rolls_input is not None
    
    submit_button = soup.find('input', {'type': 'submit', 'value': 'Ausführen'})
    assert submit_button is not None

def test_random_number_generator_ui_output(client):
    """Test if the random number generator output is displayed correctly"""
    response = client.post('/handle_tool', data={
        'tool_name': 'RandomNumberGeneratorTool',
        'Kleinste Zahl': '1',
        'Größte Zahl': '10',
        'Anzahl der Würfe': '5'
    }, headers={'Accept-Language': 'de'})
    assert response.status_code == 200
    print("Response Data:", response.data.decode('utf-8')) # Add this line to debug

    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Get the h1 heading directly from soup
    h1 = soup.find('h1')
    assert h1 is not None, "H1 heading not found"
    assert h1.text.strip() == "Zufallszahlengenerator", "Unexpected heading text"

    # Find the div containing the tool output directly from soup
    output_div = soup.find('div', {'class': 'tool-output'})
    assert output_div is not None, "Tool output div not found"

    # Find the container (still needed for other assertions if any, but not for output_div)
    container = soup.find('div', {'class': 'container'})
    assert container is not None, "Container div not found"
    
    output_text = output_div.text.strip()
    assert output_text, "Random number output is empty"
    
    # Split by commas and remove any whitespace
    number_strings = [num.strip() for num in output_text.split(',') if num.strip()]
    
    assert len(number_strings) == 5, f"Expected 5 numbers, got {len(number_strings)}: {number_strings}"
    
    for num_str in number_strings:
        try:
            num_val = int(num_str)
            assert 1 <= num_val <= 10, f"Number {num_val} is outside range 1-10"
        except ValueError:
            assert False, f"Expected integer but got: '{num_str}'"
    
    print(f"Validated random numbers: {number_strings}")
