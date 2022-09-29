# Experiment Tracker
# pdm run zenml experiment-tracker register mlflow_experiment_tracker --flavor=mlflow --tracking_username='{{mlflow_secret.username}}' --tracking_password='{{mlflow_secret.password}}' --tracking_uri=http://localhost:5000
# Data Validator
pdm run zenml data-validator register evidently_validator --flavor=evidently
# Model deployer
# pdm run zenml model-deployer register mlflow_deployer --flavor=mlflow
# Orchestrator
pdm run zenml orchestrator register kubeflow_orchestrator --flavor=kubeflow --skip_local_validations=True
# Metadata store
# pdm run zenml metadata-store register kubeflow_metadata_store --flavor=kubeflow
# Artifact Store
# pdm run zenml artifact-store register minio_store --flavor=s3 --path=s3://mlops-artifact-store --authentication_secret=s3_secret --client_kwargs='{"endpoint_url":"http://127.0.0.1:9000"}'
# Secret Manager
# pdm run zenml secrets-manager register local_secret_manager --flavor=local
# pdm run zenml secrets-manager register vault_sm --flavor=vault --url=http://127.0.0.1:8200 --token=vault-plaintext-root-token --mount_point=pipeline_secrets/
# Container Registry (ensure right hosts definition in linux &/or windows & no docker desktop credsStore)
pdm run zenml container-registry register local_container_registy --flavor=default --uri=k3d-zenml-kubeflow-registry.localhost:8000
# pdm run zenml container-registry register dockerhub_registry --flavor=dockerhub --uri=thomasbinder
# Stack update
pdm run zenml stack update default -dv evidently_validator -o kubeflow_orchestrator -c local_container_registy
# pdm run zenml secrets-manager secret register s3_secret -s aws --aws_access_key_id='minio' --aws_secret_access_key='minio123'
# pdm run zenml secrets-manager secret register mlflow_secret --username='user' --password='password'
pdm run zenml stack up
echo "Make sure REGISTRY FILE is updated!"