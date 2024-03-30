import requests
from src.constants.data_constants import MABJK_URL
from src.constants.data_constants import WEATHER_URL

def test_mbajk_api_availability():
    response = requests.get(MABJK_URL)
    assert response.status_code == 200
    
def test_weather_api_availability():
    response = requests.get(WEATHER_URL)
    assert response.status_code == 200