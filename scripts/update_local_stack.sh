# Experiment Tracker
pdm run zenml experiment-tracker register mlflow_experiment_tracker --flavor=mlflow --tracking_username='{{mlflow_secret.username}}' --tracking_password='{{mlflow_secret.password}}' --tracking_uri=http://localhost:5000
# Data Validator
pdm run zenml data-validator register evidently_validator --flavor=evidently
# Model deployer
pdm run zenml model-deployer register mlflow_deployer --flavor=mlflow
# Artifact Store
pdm run zenml artifact-store register minio_store --flavor=s3 --path=s3://mlops-artifact-store --authentication_secret=s3_secret --client_kwargs='{"endpoint_url":"http://127.0.0.1:9000"}'
# Secret Manager
pdm run zenml secrets-manager register vault_sm --flavor=vault --url=http://127.0.0.1:8200 --token=vault-plaintext-root-token --mount_point=pipeline_secrets/
# Stack update
pdm run zenml stack update default -e mlflow_experiment_tracker -dv evidently_validator -d mlflow_deployer -a minio_store -x vault_sm --decouple_stores
pdm run zenml secrets-manager secret register s3_secret -s aws --aws_access_key_id='minio' --aws_secret_access_key='minio123'
pdm run zenml secrets-manager secret register mlflow_secret --username='username' --password='password'