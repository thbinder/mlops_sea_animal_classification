import warnings

from absl import logging as absl_logging
from zenml.pipelines import pipeline

warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)


@pipeline
def inference_pipeline(
    inference_data_loader,
    prediction_service_loader,
    predictor,
):
    """Basic inference pipeline."""

    inference_data = inference_data_loader()
    model_deployment_service = prediction_service_loader()
    predictor(model_deployment_service, inference_data)
