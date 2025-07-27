from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
)
import pandas as pd

# This function evaluates the condition of data drift by comparing reference and current datasets.
# It is meant to trigger a re-training of the model in the Mage pipeline if significant drift is detected


def evaluate_condition(data):
    # Data: expects a dictionary with 'reference' and 'current' DataFrames
    reference_data = data["reference"]
    current_data = data["current"]

    # Create and run the data drift report
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=reference_data, current_data=current_data)

    # Get dataset drift detection result as boolean
    drift_result = report.as_dict()["metrics"][0]["result"]["dataset_drift"]
    if drift_result == True:
        print("significant data drift detected")
    else:
        print("no significant data drift detected")
    return drift_result
