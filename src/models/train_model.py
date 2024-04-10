from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.callbacks import CSVLogger
from src.models.utils import helper
from src.constants.data_constants import train_data_path
from src.constants.model_constants import model_path
from src.constants.model_constants import train_report_path
from src.constants.model_constants import window_size


def build_model(input_shape):
    print('Model build in process.')
    model = Sequential([
        SimpleRNN(window_size, input_shape=input_shape),
        Dense(input_shape[1])
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
    train_df = helper.load_data(train_data_path)
    csv_logger = CSVLogger(train_report_path)

    X_train, y_train = helper.to_sequence(train_df)
    
    train_model(X_train, y_train, (window_size, len(train_df.columns)), csv_logger, model_path)

if __name__ == '__main__':
    main()