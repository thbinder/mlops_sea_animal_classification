# Experiment Tracker
pdm run zenml experiment-tracker register local_mlflow_tracker --flavor=mlflow
# Data Validator
pdm run zenml data-validator register local_evidently_validator --flavor=evidently
# Model deployer
pdm run zenml model-deployer register local_mlflow_deployer --flavor=mlflow
# Artifact Store
pdm run zenml artifact-store register local_artifact_store --flavor=local
# Orchestrator
pdm run zenml orchestrator register local_orchestrator --flavor=local
# Stack registration & activation
pdm run zenml stack register local_stack -o local_orchestrator -e local_mlflow_tracker -dv local_evidently_validator -d local_mlflow_deployer -a local_artifact_store
pdm run zenml stack set local_stack