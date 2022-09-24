from zenml.repository import Repository
from zenml.services import BaseService
from zenml.steps import BaseStepConfig, step


class PredictionServiceLoaderConfig(BaseStepConfig):
    """Prediction Loading params"""

    pipeline_name: str = "training_pipeline"
    pipeline_step_name: str = "mlflow_model_deployer_step"


@step(enable_cache=False)
def prediction_service_loader(
    config: PredictionServiceLoaderConfig,
) -> BaseService:
    """Load the model service of our training pipeline."""

    repo = Repository(skip_repository_check=True)
    model_deployer = repo.active_stack.model_deployer
    services = model_deployer.find_model_server(
        pipeline_name=config.pipeline_name,
        pipeline_step_name=config.pipeline_step_name,
        running=True,
    )
    service = services[0]
    return service
