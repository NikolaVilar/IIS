import math
import pandas as pd
from src.constants.data_constants import mbajk_source
from src.constants.data_constants import mbajk_api_source
from src.constants.data_constants import weather_api_source
from src.constants.data_constants import mbajk_dataset_path
from src.constants.data_constants import mbajk_api_data_path
from src.constants.data_constants import weather_api_data_path
from src.constants.data_constants import processed_data_path
from src.constants.data_constants import datetime_format


def convert_datetime(df, source):
    if source == mbajk_api_source:
        df = df[['last_update', 'available_bike_stands', ]].copy()
        df['date'] = pd.to_datetime(df['last_update'], unit='ms')
        df = df.drop(columns='last_update')
    elif source == mbajk_source:
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime(datetime_format)
        df['date'] = pd.to_datetime(df['date'])
    else:
        df['date'] = pd.to_datetime(df['time'])
        df['date'] = df['date'].dt.strftime(datetime_format)
        df['date'] = pd.to_datetime(df['date'])
        df = df.drop(columns='time')
    return df

def get_columns(source):
    if source == mbajk_source:
        return ['available_bike_stands','temperature','relative_humidity','dew_point']
    elif source == weather_api_source:
        return ['temperature','relative_humidity','dew_point']
    return ['available_bike_stands']

def group_mean(df, columns):
    df = df.groupby('date_hour', as_index=False)[columns].mean()

    for col in columns:
        df[col] = df[col].round(2)

    return df

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
    mbajk_dataset = aggregate_data(mbajk_dataset_path, mbajk_source)
    mbajk_api_data = aggregate_data(mbajk_api_data_path, mbajk_api_source)
    weather_api_data = aggregate_data(weather_api_data_path, weather_api_source)

    mbajk_api_data = pd.merge(mbajk_api_data, weather_api_data, on='date_hour', how='inner')

    save_data(mbajk_dataset, mbajk_api_data, processed_data_path)


if __name__ == '__main__':
    main()