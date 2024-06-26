from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from src.constants.model_constants import window_size
from src.constants.model_constants import columns
from src.constants.data_constants import reference_data_path
from src.serve.utils import is_complete
from src.models.utils import helper
import pandas as pd
import numpy as np
import pymongo
import os

mlflow = helper.mlflow_setup()
model = helper.load_production_model(mlflow, 'SimpleRNN-Test')
pipeline = helper.load_pipeline(mlflow, 'SimpleRNN-Train')


mongo_uri = os.environ['MONGO_URI']
mongo_uri = mongo_uri.replace('"', '')
clientdb = pymongo.MongoClient(mongo_uri)
db = clientdb.IIS
col = db.record

app = Flask(__name__)


def predict(X):
    y_pred = model.predict(X)

    y_pred = pipeline.inverse_transform(y_pred)  
    y_pred = y_pred.astype(float)
    y_pred = np.round(y_pred, 2)
    y_pred[:, 0] = np.floor(y_pred[:, 0])


    return y_pred

@app.route('/mbajk/predict', methods=['GET'])
@cross_origin()
def get_prediction():
    df = helper.load_data(reference_data_path)

    X_test = helper.get_latest_values(df, mlflow, 'SimpleRNN-Test')
    X_test = (pipeline.transform(X_test)).reshape(-1, window_size, len(columns))
    prediction = predict(X_test)

    json_response = {
        'hours': helper.generate_hours(len(prediction)),
        'available_bike_stands': prediction[:, 0].tolist(), 
        'temperature': prediction[:, 1].tolist(), 
        'relative_humidity': prediction[:, 2].tolist(), 
        'dew_point': prediction[:, 3].tolist()
        }
    
    col.insert_one(json_response.copy())

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
    
    X = pipeline.transform(df)
    X = X.reshape(-1, window_size, len(columns))

    prediction = predict(X)

    json_response = {
        'hours': helper.generate_hours(len(prediction)),
        'available_bike_stands': prediction[:, 0].tolist(), 
        'temperature': prediction[:, 1].tolist(), 
        'relative_humidity': prediction[:, 2].tolist(), 
        'dew_point': prediction[:, 3].tolist()
        }
    
    col.insert_one(json_response.copy())

    print(json_response)
    return jsonify(json_response), 200


def main():
    app.run(host='0.0.0.0', port=5000)
    CORS(app)


if __name__ == '__main__':
    main()