import json
import math
import pandas as pd
import os


def aggregate_data(data_path, fresh=False):
    df = pd.read_csv(data_path)

    if fresh == True:
        df = df[['last_update', 'available_bike_stands', ]].copy()
        df['date'] = pd.to_datetime(df['last_update'], unit='ms')
        df = df.drop(columns='last_update')
    else:
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['date'] = pd.to_datetime(df['date'])
        df = df[['date', 'available_bike_stands']]

    
    df['date_hour'] = df['date'].dt.floor('h')
    result = df.groupby('date_hour')['available_bike_stands'].mean().reset_index()
    result['available_bike_stands'] = result['available_bike_stands'].apply(math.floor)

    print(f'Data aggregation complete: {data_path}')
    return result
    

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    dataset_path = os.path.join(root_dir, 'data', 'raw', 'mbajk_dataset.csv')
    data_api_path = os.path.join(root_dir, 'data', 'raw', 'mbajk_api.csv')
    processed_data_path = os.path.join(root_dir, 'data', 'processed', 'data.csv')

    df = pd.concat([aggregate_data(dataset_path), aggregate_data(data_api_path, fresh=True)], axis=0).reset_index(drop=True)
    df = df.sort_values(by='date_hour')
    df.to_csv(processed_data_path)


if __name__ == '__main__':
    main()