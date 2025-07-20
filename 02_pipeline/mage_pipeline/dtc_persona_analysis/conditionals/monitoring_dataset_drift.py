if 'condition' not in globals():
    from mage_ai.data_preparation.decorators import condition

from evidently.report import Report
from evidently import ColumnMapping 
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
import pandas as pd

@condition
def evaluate_condition(data, *args, **kwargs) -> bool:
    # Get data from previous block
    reference_data = data['reference']
    current_data = data['current']

    # Create and run the data drift report
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=reference_data, current_data=current_data)
    
    # Get dataset drift detection result as boolean
    drift_result = report.as_dict()["metrics"][0]["result"]["dataset_drift"]
    if drift_result == True:
        print('significant data drift detected')
    else:
        print('no significant data drift detected')
    return drift_result
