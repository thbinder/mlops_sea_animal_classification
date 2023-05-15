import os
import warnings

from absl import logging as absl_logging
from dotenv import load_dotenv
from zenml.config import DockerSettings
from zenml.integrations.kserve.services import KServeDeploymentConfig
from zenml.integrations.kserve.steps import (
    KServeDeployerStepParameters,
    kserve_model_deployer_step,
)
from zenml.pipelines import pipeline

from src.domain.steps.data_loader import gcp_train_data_loader
from src.domain.steps.deployment_trigger import deployment_trigger
from src.domain.steps.mlflow_evaluator import evaluate_classifier
from src.domain.steps.mlflow_trainer import train_classifier

# Configure warnings
warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)

docker_settings = DockerSettings(
    dockerignore="./.dockerignore",
    requirements="./requirements.txt",
    install_stack_requirements=False,
)

# kserve deployment step settings
kserve_deployer = kserve_model_deployer_step(
    KServeDeployerStepParameters(
        service_config=KServeDeploymentConfig(
            model_name="sea-animals-classifier",
            replicas=1,
            predictor="tensorflow",
            resources={"requests": {"cpu": "200m", "memory": "500m"}},
        ),
        timeout=120,
    )
)


@pipeline(
    enable_cache=False,
    settings={"docker": docker_settings},
)
def gcp_deployment_pipeline(
    load_data, train_model, evaluate_model, deployment_trigger, model_deployer
):
    load_dotenv()
    train_df, test_df = load_data()
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)
    deployment_decision = deployment_trigger(test_acc)
    model_deployer(
        deploy_decision=deployment_decision,
        model=model,
    )

    return test_acc


if __name__ == "__main__":
    pipeline = gcp_deployment_pipeline(
        load_data=gcp_train_data_loader(),
        train_model=train_classifier(),
        evaluate_model=evaluate_classifier(),
        deployment_trigger=deployment_trigger(),
        model_deployer=kserve_deployer(),
    )
    pipeline.run()
