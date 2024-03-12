import os

root_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..'))

train_report_path = os.path.join(root_dir, 'reports', 'train_metrics.txt')
test_report_path = os.path.join(root_dir, 'reports', 'metrics.txt')
model_path = os.path.join(root_dir, 'models', 'simple-rnn.h5')

window_size = 12