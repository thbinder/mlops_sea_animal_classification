# Experiment Tracker
pdm run zenml experiment-tracker register mlflow_experiment_tracker --flavor=mlflow --tracking_username='{{mlflow_secret.username}}' --tracking_password='{{mlflow_secret.password}}' --tracking_uri=http://localhost:5000
# Artifact Store
pdm run zenml artifact-store register minio_store --flavor=s3 --path=s3://mlops-artifact-store --authentication_secret=s3_secret --client_kwargs='{"endpoint_url":"http://127.0.0.1:9000"}'
# Secret Manager
pdm run zenml secrets-manager register local_sm --flavor=local
# Metadata store
pdm run zenml metadata-store register local_metadata_store --flavor=sqlite
# Orchestrator
pdm run zenml orchestrator register local_orchestrator --flavor=local
# Stack registration & activation
pdm run zenml stack register simple_stack -o local_orchestrator -m local_metadata_store -e mlflow_experiment_tracker -a minio_store -x local_sm --decouple_stores
pdm run zenml stack set simple_stack
# Register needed secrets
pdm run zenml secrets-manager secret register s3_secret -s aws --aws_access_key_id='minio' --aws_secret_access_key='minio123'
pdm run zenml secrets-manager secret register mlflow_secret --username='username' --password='password'