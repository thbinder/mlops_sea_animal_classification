import warnings

from absl import logging as absl_logging
from dotenv import load_dotenv
from zenml.integrations.mlflow.steps import (
    MLFlowDeployerParameters,
    mlflow_model_deployer_step,
)
from zenml.pipelines import pipeline

from src.domain.steps.data_loader import train_data_loader
from src.domain.steps.deployment_trigger import deployment_trigger
from src.domain.steps.mlflow_evaluator import evaluate_classifier
from src.domain.steps.mlflow_trainer import train_classifier
from src.domain.steps.skew_detector import evidently_skew_detector

# Configure warnings
warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)


@pipeline(enable_cache=False)
def train_continuous_deployment_pipeline(
    load_data,
    skew_detector,
    train_model,
    evaluate_model,
    deployment_trigger,
    model_deployer,
):

    load_dotenv()
    train_df, test_df = load_data()
    skew_detector(train_df, test_df)
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)
    deployment_decision = deployment_trigger(test_acc)
    model_deployer(deploy_decision=deployment_decision, model=model)

    return test_acc


if __name__ == "__main__":

    pipeline = train_continuous_deployment_pipeline(
        load_data=train_data_loader(),
        skew_detector=evidently_skew_detector(),
        train_model=train_classifier(),
        evaluate_model=evaluate_classifier(),
        deployment_trigger=deployment_trigger(),
        model_deployer=mlflow_model_deployer_step(MLFlowDeployerParameters(timeout=20)),
    )
    pipeline.run()
