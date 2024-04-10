from src.constants.data_constants import reference_data_path
from src.constants.data_constants import current_data_path
from src.constants.data_constants import report_path
from src.models.utils import helper
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.test_suite import TestSuite
from evidently.tests import *
import sys
import json

def test_stability(reference_df, current_df):
    report = Report(metrics=[
        DataDriftPreset(),
    ])
    
    report.run(reference_data=reference_df, current_data=current_df)
    report.save_html(report_path)

    tests = TestSuite(tests=[
        TestNumberOfColumnsWithMissingValues(),
        TestNumberOfRowsWithMissingValues(),
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType(),
        TestNumberOfDriftedColumns(),
    ])

    tests.run(reference_data=reference_df, current_data=current_df)
    result = tests.as_dict()
    print(json.dumps(result, indent=4))

    if not result["summary"]["all_passed"]:
        print("Data stability failed!")
        sys.exit(1)

    print("Data stability succeeded!")
    sys.exit(0)

def main():
    current_df = helper.load_data(current_data_path)
    reference_df = helper.load_data(reference_data_path)
    
    current_df = helper.set_column_types(current_df)
    current_df = helper.to_test(current_df)
    
    reference_df = helper.set_column_types(reference_df)
    reference_df = helper.to_test(reference_df)
    
    test_stability(reference_df, current_df)
    

if __name__ == '__main__':
    main()