import json
import math
import pandas as pd
import os


def convert_datetime(df, source):
    if source == 'mbajk_api':
        df = df[['last_update', 'available_bike_stands', ]].copy()
        df['date'] = pd.to_datetime(df['last_update'], unit='ms')
        df = df.drop(columns='last_update')
    elif source == 'mbajk':
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['date'] = pd.to_datetime(df['date'])
    else:
        df['date'] = pd.to_datetime(df['time'])
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['date'] = pd.to_datetime(df['date'])
        df = df.drop(columns='time')
    return df

def get_columns(source):
    if source == 'mbajk':
        return ['available_bike_stands','temperature','relative_humidity','dew_point']
    elif source == 'weather_api':
        return ['temperature','relative_humidity','dew_point']
    return ['available_bike_stands']

def group_mean(df, columns):
    result = pd.DataFrame()
    result['date_hour'] = df['date_hour']

    for col in columns:
        temp_result = df.groupby('date_hour')[col].mean().reset_index()
        result = pd.merge(result, temp_result, on='date_hour', how='inner')
        result[col] = df[col].round(2)

    return result

def aggregate_data(data_path, source):
    df = pd.read_csv(data_path, index_col=0)
    df = convert_datetime(df, source)
    
    df['date_hour'] = df['date'].dt.floor('h')
    columns = get_columns(source)
    result = group_mean(df, columns)

    if 'available_bike_stands' in columns:
        result['available_bike_stands'] = result['available_bike_stands'].apply(math.floor)

    print(f'Data aggregation complete: {source}')
    return result

def save_data(mbajk_dataset, mbajk_api_data, processed_data_path):
    df = pd.concat([mbajk_dataset, mbajk_api_data], axis=0).reset_index(drop=True)
    df = df.sort_values(by='date_hour')
    df.to_csv(processed_data_path)
    

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    mbajk_dataset_path = os.path.join(root_dir, 'data', 'raw', 'mbajk', 'mbajk_dataset.csv')
    mbajk_api_path = os.path.join(root_dir, 'data', 'raw', 'mbajk', 'mbajk_api.csv')
    weather_api_path = os.path.join(root_dir, 'data', 'raw', 'weather', 'weather_api.csv')
    processed_data_path = os.path.join(root_dir, 'data', 'processed', 'data.csv')

    mbajk_dataset = aggregate_data(mbajk_dataset_path, 'mbajk')
    mbajk_api_data = aggregate_data(mbajk_api_path, 'mbajk_api')
    weather_api_data = aggregate_data(weather_api_path, 'weather_api')

    mbajk_api_data = pd.merge(mbajk_api_data, weather_api_data, on='date_hour', how='inner')

    save_data(mbajk_dataset, mbajk_api_data, processed_data_path)


if __name__ == '__main__':
    main()