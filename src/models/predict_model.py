from sklearn import metrics
from src.models.utils import reshaper
from tensorflow.keras.models import load_model
import os


def evaluate_model(X_test, y_test, model, report_path):
    print('Model evaluation in process.')

    y_pred = model.predict(X_test)
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    evs = metrics.explained_variance_score(y_test, y_pred)
    
    with open(report_path, 'w') as file:
        file.write(f'MAE:{mae}\nMSE:{mse}\nEVS:{evs}')

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    data_path = os.path.join(root_dir, 'data', 'processed', 'data.csv')
    test_report_path = os.path.join(root_dir, 'reports', 'metrics.txt')
    model_path = os.path.join(root_dir, 'models', 'simple-rnn.h5')
    window_size = 12
    
    df = reshaper.load_data(data_path)

    X_train, y_train, X_test, y_test = reshaper.test_train_split(df, window_size)
    model = load_model(model_path)
    evaluate_model(X_test, y_test, model, test_report_path)

if __name__ == '__main__':
    main()