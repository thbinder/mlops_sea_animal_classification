from pathlib import Path
from typing import List
import logging
import cv2
import numpy as np
from zenml.pipelines import pipeline
from zenml.repository import Repository
from zenml.services import BaseService
from zenml.steps import BaseStepConfig, Output, step
from src.domain.class_mapping import class_mapping

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

class InferenceDataLoaderConfig(BaseStepConfig):
    """Data Loading params"""

    target_shape: List[int] = [224, 224, 3]
    data_path: str = "./test_data"


class PredictionServiceLoaderConfig(BaseStepConfig):
    """Prediction Loading params"""

    pipeline_name: str = "training_pipeline"
    pipeline_step_name: str = "mlflow_model_deployer_step"


@step
def inference_data_loader(
    config: InferenceDataLoaderConfig,
) -> np.ndarray:
    """Load some inference data."""

    def load_and_preprocess_image(img_path):
        img = cv2.imread(img_path, 0)
        img = cv2.resize(img, (config.target_shape[0], config.target_shape[1]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img, dtype=np.float32).reshape(
            1, config.target_shape[0], config.target_shape[1], config.target_shape[2]
        )
        return img

    data_dir = Path(config.data_path)
    filepaths = (
        list(data_dir.glob(r"**/*.JPG"))
        + list(data_dir.glob(r"**/*.jpg"))
        + list(data_dir.glob(r"**/*.png"))
        + list(data_dir.glob(r"**/*.PNG"))
    )

    first_image_flag = True
    for img_path in filepaths:

        img_path = str(img_path)
        if first_image_flag:
            imgs_array = load_and_preprocess_image(img_path)
            first_image_flag = False
        else:
            img = load_and_preprocess_image(img_path)
            imgs_array = np.concatenate((imgs_array, img), axis=0)

    return imgs_array


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


@step
def predictor(
    service: BaseService,
    data: np.ndarray,
) -> Output(predictions=list):
    """Run a inference request against a prediction service"""
    service.start(timeout=10)  # should be a NOP if already started
    predictions = service.predict(data)
    predictions = predictions.argmax(axis=1)
    results = list()
    for pred in predictions:
        results.append(class_mapping[pred])
    logger.info(results)

    return results


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
