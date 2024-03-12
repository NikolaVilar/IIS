import numpy as np
import pandas as pd
from src.constants.model_constants import window_size


def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data


def build_sequences(df):
    print('Sequence build in process.')

    X = []
    y = []

    df = df.drop(columns=['date_hour'])

    for i in range(len(df) - window_size):
        X.append(df.iloc[i:i+window_size].values)
        y.append(df.iloc[i+window_size].values)  
    X = np.array(X)
    y = np.array(y)
    return X, y


def test_train_split(df):
    print('Test, train split in process.')

    split_index = len(df) - (7 * window_size)
    
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train, y_train = build_sequences(train_df)
    X_test, y_test = build_sequences(test_df)

    return X_train.reshape(-1, window_size, len(df.columns)-1), y_train, X_test.reshape(-1, window_size, len(df.columns)-1), y_test