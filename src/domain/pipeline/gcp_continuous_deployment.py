import warnings

from absl import logging as absl_logging
from dotenv import load_dotenv
from zenml.pipelines import pipeline

from src.domain.steps.data_loader import gcp_train_data_loader
from src.domain.steps.deployment_trigger import deployment_trigger
from src.domain.steps.mlflow_evaluator import evaluate_classifier
from src.domain.steps.mlflow_trainer import train_classifier
from zenml.config import DockerSettings

# Configure warnings
warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)

docker_settings = DockerSettings(dockerignore="/path/to/.dockerignore",
                                requirements="./requirements.txt")


@pipeline(enable_cache=False)
def gcp_continuous_deployment_pipeline(
    load_data,
    train_model,
    evaluate_model,
    deployment_trigger,
):

    load_dotenv()
    train_df, test_df = load_data()
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)
    deployment_decision = deployment_trigger(test_acc)

    return test_acc


if __name__ == "__main__":

    pipeline = gcp_continuous_deployment_pipeline(
        load_data=gcp_train_data_loader(),
        train_model=train_classifier(),
        evaluate_model=evaluate_classifier(),
        deployment_trigger=deployment_trigger(),
    )
    pipeline.run()
