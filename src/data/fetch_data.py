import json
import requests
import pandas as pd
import os

URL = "https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b"


def fetch_api():
    data = []
    print(f'GET: {URL}')
    response = requests.get(URL)
    if response.status_code == 200:
        print("Successfully retrieved data")
        data = json.loads(response.content)
    else:
        print("Failed to retrieve JSON data")

    filtered_data = [record for record in data if record.get('name') == "GOSPOSVETSKA C. - TURNERJEVA UL."]
    return filtered_data

def merge_data(ndf, data_path):
    df = pd.read_csv(data_path, index_col=0)
    last_update = ndf['last_update'].values[0]
    if last_update not in df['last_update'].values:
        df = pd.concat([df, ndf], axis=0).reset_index(drop=True)
    return df


def save_data(data, data_path):
    for record in data:
        position = record.pop('position')  
        record['lat'] = position['lat'] 
        record['lng'] = position['lng'] 

    df = pd.DataFrame(data)
    df = merge_data(df, data_path)
    df.to_csv(data_path)


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    data_path = os.path.join(root_dir, 'data', 'raw', 'mbajk_api.csv')
    data = fetch_api()
    save_data(data, data_path)

if __name__ == '__main__':
    main()