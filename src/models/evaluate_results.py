from src.models.utils import helper
from src.constants.data_constants import reference_data_path
from src.constants.model_constants import MLFLOW_TRACKING_URI
from sklearn import metrics
import pandas as pd
import pymongo
import mlflow
import os

def get_collection():
    mongo_uri = os.environ['MONGO_URI']
    mongo_uri = mongo_uri.replace('"', '')
    clientdb = pymongo.MongoClient(mongo_uri)
    db = clientdb.IIS
    col = db.record
    return col

def get_predictions(col):
    all_records = col.find()
    df = pd.DataFrame()

    for record in all_records:
        record.pop('_id', None)
        t = pd.DataFrame.from_dict(record, orient='index').T
        df = pd.concat([df, t], ignore_index=True)

    df['hours'] = pd.to_datetime(df['hours']) 
    average_by_datetime = df.groupby(df['hours']).mean()
    average_by_datetime = average_by_datetime.reset_index()
    df = average_by_datetime.copy()

    df = df.drop(columns=['temperature', 'relative_humidity', 'dew_point'])
    df = df.rename(columns={'hours': 'date_hour'})
    return df

def get_true_values():
    y_true = helper.load_data(reference_data_path)
    y_true.reset_index(inplace=True)
    y_true['date_hour'] = pd.to_datetime(y_true['date_hour'])
    return y_true

def log_metrics(y_true, y_pred):
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("bike-rental-evaluation")
    
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    evs = metrics.explained_variance_score(y_true, y_pred)
    
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("evs", evs)

def main():    
    col = get_collection()
    y_pred = get_predictions(col)
    y_true = get_true_values()
    
    merged_df = pd.merge(y_true, y_pred, on='date_hour', how='inner')
    log_metrics(merged_df['available_bike_stands_x'], merged_df['available_bike_stands_y'])
    
    

if __name__ == '__main__':
    main()