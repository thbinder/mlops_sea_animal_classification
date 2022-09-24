pdm run zenml secrets-manager register local_secret_manager --flavor=local
pdm run zenml experiment-tracker register mlflow_experiment_tracker --flavor=mlflow --tracking_username='{{mlflow_secret.username}}' --tracking_password='{{mlflow_secret.password}}' --tracking_uri=http://localhost:5000
pdm run zenml model-deployer register mlflow_deployer --flavor=mlflow
pdm run zenml data-validator register evidently_validator --flavor=evidently
pdm run zenml stack update default -x local_secret_manager -d mlflow_deployer -e mlflow_experiment_tracker -dv evidently_validator
pdm run zenml stack register-secrets default