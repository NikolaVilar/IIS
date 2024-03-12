import os

root_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..'))

train_report_path = os.path.join(root_dir, 'reports', 'train_metrics.txt')
test_report_path = os.path.join(root_dir, 'reports', 'metrics.txt')
model_path = os.path.join(root_dir, 'models', 'simple-rnn.h5')
scaler_path = os.path.join(root_dir, 'scalers', 'standard.pkl')

window_size = 8

columns = ['available_bike_stands','temperature','relative_humidity','dew_point']