import numpy as np
import pandas as pd
from src.constants.model_constants import window_size
from src.constants.model_constants import columns
from src.constants.model_constants import scaler_path
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pickle


def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data


def build_sequences(df):
    print('Sequence build in process.')

    X = []
    y = []

    for i in range(len(df) - window_size):
        X.append(df.iloc[i:i+window_size].values)
        y.append(df.iloc[i+window_size].values)  
    X = np.array(X)
    y = np.array(y)
    return X, y

def scale_data_training(train_df, test_df, columns, scaler_path):
    scaler = StandardScaler()
    train_df = scaler.fit_transform(train_df)
    test_df = scaler.transform(test_df)

    train_df = pd.DataFrame(train_df, columns=columns)
    test_df = pd.DataFrame(test_df, columns=columns)

    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    return train_df, test_df


def unscale_data(data, scaler_path):
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    data = scaler.inverse_transform(data)    
    return data.astype(float)

def scale_data(data, scaler_path):
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    data = scaler.transform(data)    
    return data

def to_sequence(df):
    print('Sequence build in progress.')
    X, y = build_sequences(df)
    return X.reshape(-1, window_size, len(df.columns)), y

def get_latest_values(df):
    split_index = len(df) - (7 * window_size)

    test = df.iloc[split_index:]
    test = scale_data(test, scaler_path)

    return test.reshape(-1, window_size, len(columns))

def generate_hours(n):
    current_time = datetime.now().replace(second=0, microsecond=0, minute=0)
    datetime_values = [(current_time + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M') for i in range(n)]
    return datetime_values

    

