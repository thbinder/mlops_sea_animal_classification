import warnings

from absl import logging as absl_logging
from zenml.pipelines import pipeline

warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)


@pipeline(enable_cache=False)
def local_inference_pipeline(
    local_inference_data_loader,
    prediction_service_loader,
    predictor,
):
    """Basic inference pipeline."""

    inference_data = local_inference_data_loader()
    model_deployment_service = prediction_service_loader()
    predictor(model_deployment_service, inference_data)
