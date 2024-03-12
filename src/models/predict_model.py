from sklearn import metrics
from src.models.utils import reshaper
from tensorflow.keras.models import load_model
from src.constants.data_constants import processed_data_path
from src.constants.model_constants import model_path
from src.constants.model_constants import test_report_path

def evaluate_model(X_test, y_test, model, report_path):
    print('Model evaluation in process.')

    y_pred = model.predict(X_test)
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    evs = metrics.explained_variance_score(y_test, y_pred)
    
    with open(report_path, 'w') as file:
        file.write(f'MAE:{mae}\nMSE:{mse}\nEVS:{evs}')

def main():
    df = reshaper.load_data(processed_data_path)
    X_train, y_train, X_test, y_test = reshaper.test_train_split(df)
    model = load_model(model_path)
    evaluate_model(X_test, y_test, model, test_report_path)

if __name__ == '__main__':
    main()