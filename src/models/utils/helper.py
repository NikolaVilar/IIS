from src.constants.model_constants import window_size
from src.constants.model_constants import columns
from src.constants.model_constants import train_report_path
from src.constants.model_constants import pipeline_path
from src.constants.model_constants import MLFLOW_TRACKING_URI
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np
import pandas as pd
import mlflow
from mlflow.models.signature import infer_signature
from mlflow import MlflowClient

def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data

def load_pipeline(mlflow, name):
    client = MlflowClient()
    run_id = client.get_registered_model(name).latest_versions[0].run_id
    pipeline = mlflow.sklearn.load_model(f'runs:/{run_id}/pipeline')
    return pipeline

def load_model(mlflow, name):
    client = MlflowClient()
    run_id = client.get_registered_model(name).latest_versions[0].run_id
    model = mlflow.pyfunc.load_model(f'runs:/{run_id}/{name}')
    return model

def load_production_model(mlflow, name):
    model_uri = f"models:/{name}@production"
    model = mlflow.pyfunc.load_model(model_uri)
    return model

def set_column_types(df):
    df['available_bike_stands'] = df['available_bike_stands'].astype(int)
    df['temperature'] = df['temperature'].astype(float)
    df['relative_humidity'] = df['relative_humidity'].astype(float)
    df['dew_point'] = df['dew_point'].astype(float)
    return df

def to_test(df):
    df.rename(columns={'available_bike_stands': 'target'}, inplace=True)
    df['prediction'] = df['target'].values + np.random.normal(0, 5, df.shape[0])
    return df

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

def preprocess_data_training(train_df, mlflow):
    pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])
    train_df = pipeline.fit_transform(train_df)
    train_df = pd.DataFrame(train_df, columns=columns)
    
    mlflow.sklearn.log_model(pipeline, 'pipeline')
    return train_df

def preprocess_data_testing(test_df, mlflow, name):
    pipeline = load_pipeline(mlflow, name)
    test_df = pipeline.transform(test_df)
    test_df = pd.DataFrame(test_df, columns=columns)
    return test_df
    
def unscale_data(data, mlflow, name):
    pipeline = load_pipeline(mlflow, name)
    data = pipeline.inverse_transform(data)    
    return data.astype(float)

def scale_data(data, mlflow, name):
    pipeline = load_pipeline(mlflow, name)
    data = pipeline.transform(data)    
    return data

def to_sequence(df):
    print('Sequence build in progress.')
    X, y = build_sequences(df)
    return X.reshape(-1, window_size, len(df.columns)), y

def get_latest_values(df, mlflow, name):
    split_index = len(df) - (7 * window_size)

    test = df.iloc[split_index:]
    
    return test

def generate_hours(n):
    current_time = datetime.now().replace(second=0, microsecond=0, minute=0)
    datetime_values = [(current_time + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M') for i in range(n)]
    return datetime_values
 
def mlflow_setup():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("bike-rental")
    return mlflow
    
def mlflow_log_metrics(y_test, y_pred, mlflow):
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    evs = metrics.explained_variance_score(y_test, y_pred)
    
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("evs", evs)
    
    return mae, mse, evs
    
def mlflow_log_model(model, name, X, mlflow):
    signature = infer_signature(X, model.predict(X))
    mlflow.sklearn.log_model(model, signature=signature, artifact_path=name,
                             registered_model_name=name)

def mlflow_log_train_loss(mlflow):
    mlflow.log_artifact(train_report_path)

 
def get_best_run(mlflow):
    all_runs = mlflow.search_runs(search_all_experiments=True)
    best_run = all_runs.iloc[all_runs['metrics.mse'].idxmin()]
    return best_run['run_id']
 
def get_model_version_from_run_id(model_name, run_id):
    client = MlflowClient()
    model_versions = client.search_model_versions(f"name='{model_name}'")

    for model_version in model_versions:
        print(model_version)
        if model_version.run_id == run_id:
            return model_version.version

    return None
 
def mlflow_promote_model(mlflow):
    client = MlflowClient()
    best_run = get_best_run(mlflow)
    version = get_model_version_from_run_id('SimpleRNN-Test', best_run)
    client.set_registered_model_alias('SimpleRNN-Test', "production", version)
