from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
import numpy as np
import math
import os


window_size = 12

app = Flask(__name__)

def predict(X):
    root_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..'))
    model_path = os.path.join(root_dir, 'models', 'simple-rnn.h5')
    model = load_model(model_path)
    y_pred = model.predict(X)
    return y_pred



@app.route('/mbajk/predict', methods=['POST'])
@cross_origin()
def predict_endpoint():
    data = request.json.get('data')
    if data is None:
        return jsonify({'error': 'Data not found in request body'}), 400
    
    data_array = np.array(data)
    
    if len(data_array) < window_size:
        return jsonify({'error': f'Data length must be at least {window_size}'}), 400
    

    X = data_array.reshape(1, -1)
    prediction = predict(X).reshape(1, )
    prediction = math.floor(prediction)
    print(prediction)

    return jsonify({'prediction': prediction}), 200


def main():
    app.run(host='0.0.0.0', port=5000)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})



if __name__ == '__main__':
    main()