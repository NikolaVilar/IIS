import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.callbacks import CSVLogger
from sklearn import metrics
import os


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def build_model(input_shape):
    model = Sequential([
        SimpleRNN(10, input_shape=input_shape),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def build_sequences(df, window_size):
    print('Sequence build in process.')

    X = []
    y = []

    for i in range(len(df) - window_size):
        X.append(df['available_bike_stands'].iloc[i:i+window_size])
        y.append(df['available_bike_stands'].iloc[i+window_size])
    X = np.array(X)
    y = np.array(y)
    return X, y


def test_train_split(df, window_size):
    print('Test, train split in process.')

    split_index = len(df) - (7 * window_size)
    
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train, y_train = build_sequences(train_df, window_size)
    X_test, y_test = build_sequences(test_df, window_size)

    return X_train.reshape(-1, window_size, 1), y_train, X_test.reshape(-1, window_size, 1), y_test


def train_model(X_train, y_train, input_shape, logger, model_path):
    print('Model training in process.')

    model = build_model(input_shape)
    model.fit(X_train, y_train, epochs=10, batch_size=32, callbacks=[logger])
    model.save(model_path)
    return model


def evaluate_model(X_test, y_test, model, report_path):
    print('Model evaluation in process.')

    y_pred = model.predict(X_test)
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    evs = metrics.explained_variance_score(y_test, y_pred)
    
    with open(report_path, 'w') as file:
        file.write(f'MAE:{mae}\nMSE:{mse}\nEVS:{evs}')


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    data_path = os.path.join(root_dir, 'data', 'processed', 'data.csv')
    train_report_path = os.path.join(root_dir, 'reports', 'train_metrics.txt')
    test_report_path = os.path.join(root_dir, 'reports', 'metrics.txt')
    model_path = os.path.join(root_dir, 'models', 'simple-rnn.h5')
    window_size = 12
    
    df = load_data(data_path)
    csv_logger = CSVLogger(train_report_path)

    X_train, y_train, X_test, y_test = test_train_split(df, window_size)
    model = train_model(X_train, y_train, (window_size, 1), csv_logger, model_path)
    evaluate_model(X_test, y_test, model, test_report_path)


if __name__ == '__main__':
    main()