[New Data Arrives] --> [Mage Pipeline Triggered]
      |
      V
[Step 1: Load Data & Reference]
   - Load new inference data
   - Load the "reference" dataset (from MLflow)
      |
      V
[Step 2: Drift Detection with Evidently]
   - Run Evidently TestSuite (e.g., DataDriftTestPreset)
   - Compare new data vs. reference data
      |
      V
[Step 3: Conditional Branching (Mage)] --(Drift Detected?)--> [Step 4: Retrain Model]
      |                                                            |
 (No Drift)                                                        V
      |                                                     [Step 5: Log with MLflow]
      V                                                            |
[End Pipeline / Log Status]                                        V
                                                              [Step 6: Register New Model]
                                                                   |
                                                                   V
                                                              [Step 7: Deploy (Optional)]