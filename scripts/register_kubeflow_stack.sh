# Data Validator
pdm run zenml data-validator register evidently_validator --flavor=evidently
# Orchestrator
pdm run zenml orchestrator register kubeflow_orchestrator --flavor=kubeflow --skip_local_validations=True
# Metadata store
pdm run zenml metadata-store register kubeflow_metadata_store --flavor=kubeflow
# Artifact Store
pdm run zenml artifact-store register local_artifact_store --flavor=local
# Container Registry (ensure right hosts definition in linux &/or windows)
pdm run zenml container-registry register local_container_registy --flavor=default --uri=localhost:8000
# Stack registration & activation
pdm run zenml stack register kubeflow_local_stack -a local_artifact_store -m kubeflow_metadata_store -dv evidently_validator -o kubeflow_orchestrator -c local_container_registy
pdm run zenml stack set kubeflow_local_stack
# Building stack
pdm run zenml stack up
# Change registry name (fix)
pdm run zenml container-registry update local_container_registy --uri=k3d-zenml-kubeflow-registry.localhost:8000
pdm run zenml stack update kubeflow_local_stack -c local_container_registy
pdm run zenml stack up
echo "!!! Make sure REGISTRY FILE is updated!                       !!!"
echo "!!! Make sure Docker Desktop .docker/config.json was deleted! !!!"