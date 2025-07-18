
- data: creation in jupyter notebooks / to_scripts
    reference_data (model trained on)
    new_data (to run labeling and to detect drifts)
    data sent to dockerized postgres database (Makefile?)

- model: experiment tracking (4)
    - creation in jupyter notebooks / to_scripts
    - experiment tracking in mlflow, locally
    - model registry locally, sqlite

- no pipe
    - mage pipeline to load data from postgres, run experiments, register best model to containerized tracking server
- no deploy

- monitoring: evidently: data drift and silouhette score, locally in notebooks (2)

- no reproducibility

- best practice:
    - pre-commit hooks: large_files / private_key (1)
    - TBD black


