import os

root_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..'))

mbajk_dataset_path = os.path.join(root_dir, 'data', 'raw', 'mbajk', 'mbajk_dataset.csv')
mbajk_api_data_path = os.path.join(root_dir, 'data', 'raw', 'mbajk', 'mbajk_api.csv')
weather_api_data_path = os.path.join(root_dir, 'data', 'raw', 'weather', 'weather_api.csv')
processed_data_path = os.path.join(root_dir, 'data', 'processed', 'data.csv')


MABJK_URL = "https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b"
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast?'
mbajk_source = 'mbajk'
mbajk_api_source = 'mbajk_api'
weather_api_source = 'weather_api'

datetime_format = '%Y-%m-%d %H:%M:%S'