import json
import requests
import pandas as pd
from datetime import datetime
import os

MABJK_URL = "https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b"
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast?'
lat = 0
lon = 0

def get_url():
    date = datetime.now()
    date = date.strftime('%Y-%m-%d')
    url = WEATHER_URL + f'latitude={lat}&longitude={lon}&'
    url += '&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&forecast_days=1'
    return url

def fetch_api(api):
    data = []
    url = MABJK_URL if api == 'mbajk' else get_url()
    print(f'GET: {url}')
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully retrieved data")
        data = json.loads(response.content)
    else:
        print("Failed to retrieve JSON data")
    return data
    

def to_df(data, source):
    if  source != 'mbajk':
        data = data['hourly']
        return pd.DataFrame(data)
    
    data = [record for record in data if record.get('name') == "GOSPOSVETSKA C. - TURNERJEVA UL."]
    for record in data:
        position = record.pop('position')  
        record['lat'] = position['lat'] 
        record['lng'] = position['lng'] 
    return pd.DataFrame(data)

def get_date_column(data_path):
    return "last_update" if "mbajk" in data_path else "time"

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



def main():
    global lat
    global lon

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    mbajk_data_path = os.path.join(root_dir, 'data', 'raw', 'mbajk', 'mbajk_api.csv')
    weather_data_path = os.path.join(root_dir, 'data', 'raw', 'weather', 'weather_api.csv')


    mbajk_data = fetch_api('mbajk')
    mbajk_data = to_df(mbajk_data, 'mbajk')

    lat = mbajk_data['lat'].values[0]
    lon = mbajk_data['lng'].values[0]

    weather_data = fetch_api('weather')
    weather_data = to_df(weather_data, 'weather')
    weather_data.rename(columns={'temperature_2m': 'temperature', 'relative_humidity_2m': 'relative_humidity', 'dew_point_2m':'dew_point'}, inplace=True)


    save_data(mbajk_data, mbajk_data_path)
    save_data(weather_data, weather_data_path)

if __name__ == '__main__':
    main()