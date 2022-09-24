import warnings
from typing import List

from absl import logging as absl_logging
from dotenv import load_dotenv
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step
from zenml.pipelines import pipeline

warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)


@pipeline
def training_pipeline(
    load_data,
    train_model,
    evaluate_model,
    deployment_trigger,
    model_deployer=mlflow_model_deployer_step(),
):

    load_dotenv()
    train_df, test_df = load_data()
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)
    deployment_decision = deployment_trigger(test_acc)
    model_deployer(deployment_decision, model)

    return test_acc
