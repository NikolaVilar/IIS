from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
from src.constants.model_constants import window_size
from src.constants.model_constants import columns
from src.constants.model_constants import model_path
from src.constants.model_constants import scaler_path
from src.constants.data_constants import reference_data_path
from src.serve.utils import is_complete
from src.models.utils import helper
import pandas as pd
import numpy as np


app = Flask(__name__)
CORS(app)

def predict(X):
    model = load_model(model_path)
    y_pred = model.predict(X)

    y_pred = helper.unscale_data(y_pred, scaler_path)
    y_pred = np.round(y_pred, 2)
    y_pred[:, 0] = np.floor(y_pred[:, 0])


    return y_pred

@app.route('/mbajk/predict', methods=['GET'])
@cross_origin()
def get_prediction():
    df = helper.load_data(reference_data_path)

    X_test = helper.get_latest_values(df)
    prediction = predict(X_test)

    json_response = {
        'hours': helper.generate_hours(len(prediction)),
        'available_bike_stands': prediction[:, 0].tolist(), 
        'temperature': prediction[:, 1].tolist(), 
        'relative_humidity': prediction[:, 2].tolist(), 
        'dew_point': prediction[:, 3].tolist()
        }

    print(json_response)
    return jsonify(json_response), 200


@app.route('/mbajk/predict', methods=['POST'])
@cross_origin()
def post_prediction():
    data = request.json
    if not is_complete(list(data.keys()), columns):
        return jsonify({'error': 'Missing properies of data are present.'}), 400
    
    df = pd.DataFrame(data)
    df = df.reindex(columns=columns)
    
    if len(df.values) < window_size:
        return jsonify({'error': f'Data length must be at least {window_size}'}), 400
    
    X = helper.scale_data(df, scaler_path)
    X = X.reshape(-1, window_size, len(columns))

    prediction = predict(X)

    json_response = {
        'hours': helper.generate_hours(len(prediction)),
        'available_bike_stands': prediction[:, 0].tolist(), 
        'temperature': prediction[:, 1].tolist(), 
        'relative_humidity': prediction[:, 2].tolist(), 
        'dew_point': prediction[:, 3].tolist()
        }

    print(json_response)
    return jsonify(json_response), 200


def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()