from src.serve.server import app
from src.constants.model_constants import columns

def test_get_request():
    response = app.test_client().get('/mbajk/predict')
    assert response.status_code == 200
    assert all(column in response.json for column in columns)

