import json
import requests
import pandas as pd
from datetime import datetime
from src.constants.data_constants import MABJK_URL
from src.constants.data_constants import WEATHER_URL
from src.constants.data_constants import mbajk_api_source
from src.constants.data_constants import weather_api_source
from src.constants.data_constants import mbajk_api_data_path
from src.constants.data_constants import weather_api_data_path
import os

lat = 0
lon = 0

def get_url():
    date = datetime.now()
    date = date.strftime('%Y-%m-%d')
    url = WEATHER_URL + f'latitude={lat}&longitude={lon}&'
    url += '&hourly=temperature_2m,relative_humidity_2m,dew_point_2m&forecast_days=1'
    return url

def fetch_api(api):
    data = []
    url = MABJK_URL if api == mbajk_api_source else get_url()
    print(f'GET: {url}')
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully retrieved data")
        data = json.loads(response.content)
    else:
        print("Failed to retrieve JSON data")
    return data
    

def to_df(data, source):
    if  source != mbajk_api_source:
        data = data['hourly']
        return pd.DataFrame(data)
    
    data = [record for record in data if record.get('name') == "GOSPOSVETSKA C. - TURNERJEVA UL."]
    for record in data:
        position = record.pop('position')  
        record['lat'] = position['lat'] 
        record['lng'] = position['lng'] 
    return pd.DataFrame(data)

def get_date_column(data_path):
    return "last_update" if mbajk_api_source in data_path else "time"

def merge_data(ndf, data_path):
    df = pd.read_csv(data_path, index_col=0)

    date_column = get_date_column(data_path)
    
    new_rows = ndf[~ndf[date_column].isin(df[date_column])]
    if not new_rows.empty:
        df = pd.concat([df, new_rows], axis=0).reset_index(drop=True)
    
    return df

def save_data(df, data_path):
    df = merge_data(df, data_path)
    df.to_csv(data_path)
    print("Successfully saved data")

def list_files(directory):
    files = os.listdir(directory)
    
    # Print each file
    for file in files:
        print(file)


def main():    
    global lat
    global lon

    mbajk_data = fetch_api(mbajk_api_source)
    mbajk_data = to_df(mbajk_data, mbajk_api_source)

    lat = mbajk_data['lat'].values[0]
    lon = mbajk_data['lng'].values[0]

    weather_data = fetch_api(weather_api_source)
    weather_data = to_df(weather_data, weather_api_source)
    weather_data.rename(columns={'temperature_2m': 'temperature', 'relative_humidity_2m': 'relative_humidity', 'dew_point_2m':'dew_point'}, inplace=True)

    save_data(mbajk_data, mbajk_api_data_path)
    save_data(weather_data, weather_api_data_path)

if __name__ == '__main__':
    main()