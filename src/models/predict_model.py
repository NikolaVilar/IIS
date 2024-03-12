from sklearn import metrics
from src.models.utils import helper
from tensorflow.keras.models import load_model
from src.constants.data_constants import processed_data_path
from src.constants.model_constants import model_path
from src.constants.model_constants import scaler_path
from src.constants.model_constants import test_report_path

def evaluate_model(X_test, y_test, model, report_path):
    print('Model evaluation in process.')

    y_pred = model.predict(X_test)
    y_pred = helper.unscale_data(y_pred, scaler_path)
    y_test = helper.unscale_data(y_test, scaler_path)

    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    evs = metrics.explained_variance_score(y_test, y_pred)
    
    with open(report_path, 'w') as file:
        file.write(f'MAE:{mae}\nMSE:{mse}\nEVS:{evs}')

def main():
    df = helper.load_data(processed_data_path)
    df = df.drop(columns='date_hour')
    X_train, y_train, X_test, y_test = helper.test_train_split(df)
    print(X_test.shape)
    model = load_model(model_path)
    evaluate_model(X_test, y_test, model, test_report_path)

if __name__ == '__main__':
    main()