from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.callbacks import CSVLogger
from src.constants.data_constants import train_data_path
from src.constants.model_constants import model_path
from src.constants.model_constants import train_report_path
from src.constants.model_constants import window_size
from src.models.utils import helper

mlflow = helper.mlflow_setup()

def build_model(input_shape):
    print('Model build in process.')
    model = Sequential([
        SimpleRNN(window_size, input_shape=input_shape),
        Dense(input_shape[1])
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def train_model(X_train, y_train, input_shape, model_path):
    print('Model training in process.')
    
    csv_logger = CSVLogger(train_report_path)

    model = build_model(input_shape)
    model.fit(X_train, y_train, epochs=10, batch_size=32, callbacks=[csv_logger])        
    
    helper.mlflow_log_model(model, 'SimpleRNN-Train', X_train, mlflow)
    helper.mlflow_log_train_loss(mlflow)

def main():    
    train_df = helper.load_data(train_data_path)  
    train_df = helper.preprocess_data_training(train_df, mlflow)
    
    X_train, y_train = helper.to_sequence(train_df)
        
    train_model(X_train, y_train, (window_size, len(train_df.columns)), model_path)

if __name__ == '__main__':
    main()