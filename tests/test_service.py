from src.serve.server import app
from src.constants.model_constants import columns

# def test_post_request():
#     request_data = {
#         "available_bike_stands": [0,2,7,8,6,5,8,10,11,7,4,12,0,2,7,8,6,5,8,10,11,7,4,12],
#         "temperature": [12,15,17,15,14.5,12,12.5,13,14.6,16,17,13,12,15,17,15,14.5,12,12.5,13,14.6,16,17,13],
#         "relative_humidity": [53,55,47,58,64,52,66,71,52,63,67,50,53,55,47,58,64,52,66,71,52,63,67,50],
#         "dew_point": [11.3,12.3,12.7,12.8,12.6,11.5,12.8,14.1,11,15.7,14.3,12.8,11.3,12.3,12.7,12.8,12.6,11.5,12.8,14.1,11,15.7,14.3,12.8]
#     }
#     response = app.test_client().post('/mbajk/predict', json=request_data)
    
#     assert response.status_code == 200
#     assert all(column in response.json for column in columns)

def test_get_request():
    response = app.test_client().get('/mbajk/predict')
    assert response.status_code == 200
    assert all(column in response.json for column in columns)

