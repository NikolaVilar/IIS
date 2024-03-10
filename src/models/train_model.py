from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.callbacks import CSVLogger
from src.models.utils import reshaper
import os


def build_model(input_shape):
    print('Model build in process.')
    model = Sequential([
        SimpleRNN(10, input_shape=input_shape),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def train_model(X_train, y_train, input_shape, logger, model_path):
    print('Model training in process.')

    model = build_model(input_shape)
    model.fit(X_train, y_train, epochs=10, batch_size=32, callbacks=[logger])
    model.save(model_path)
    return model


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    data_path = os.path.join(root_dir, 'data', 'processed', 'data.csv')
    train_report_path = os.path.join(root_dir, 'reports', 'train_metrics.txt')
    test_report_path = os.path.join(root_dir, 'reports', 'metrics.txt')
    model_path = os.path.join(root_dir, 'models', 'simple-rnn.h5')
    window_size = 12
    
    df = reshaper.load_data(data_path)
    csv_logger = CSVLogger(train_report_path)

    X_train, y_train, X_test, y_test = reshaper.test_train_split(df, window_size)
    train_model(X_train, y_train, (window_size, 1), csv_logger, model_path)

if __name__ == '__main__':
    main()