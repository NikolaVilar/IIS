
from src.models.utils import helper
from src.constants.data_constants import test_data_path

mlflow = helper.mlflow_setup()

def evaluate_model(X_test, y_test, model):
    print('Model evaluation in process.')
    
    helper.mlflow_setup()
    
    y_pred = model.predict(X_test)
    y_pred = helper.unscale_data(y_pred, mlflow, 'SimpleRNN-Train')
    y_test = helper.unscale_data(y_test, mlflow, 'SimpleRNN-Train')

    helper.mlflow_log_model(model,'SimpleRNN-Test', X_test, mlflow)
    helper.mlflow_log_metrics(y_test, y_pred, mlflow)
    
    helper.mlflow_promote_model(mlflow)

def main():
    test_df = helper.load_data(test_data_path)
    test_df = helper.preprocess_data_testing(test_df, mlflow, 'SimpleRNN-Train')
    
    X_test, y_test = helper.to_sequence(test_df)
    
    model = helper.load_model(mlflow, 'SimpleRNN-Train')
    evaluate_model(X_test, y_test, model)
    

if __name__ == '__main__':
    main()