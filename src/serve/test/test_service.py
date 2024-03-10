from src.serve.server import app

def test_api_server():
    request_data = {"data": [0, 2, 7, 8, 6, 5, 8, 10, 11, 7, 4, 12]}
    response = app.test_client().post('/mbajk/predict', json=request_data)
    
    assert response.status_code == 200
    assert "prediction" in response.json
