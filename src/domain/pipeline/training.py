import warnings

from absl import logging as absl_logging
from dotenv import load_dotenv
from zenml.config.docker_configuration import DockerConfiguration
from zenml.pipelines import pipeline

from src.domain.steps.data_loader import train_data_loader
from src.domain.steps.mlflow_evaluator import evaluate_classifier
from src.domain.steps.mlflow_trainer import train_classifier

####################################
####################################
####################################

# import os
# from kubernetes import client as k8s_client
# from zenml.integrations.kubeflow.orchestrators.kubeflow_orchestrator import KubeflowOrchestrator
# from zenml.integrations.kubeflow.orchestrators.kubeflow_orchestrator import KubeflowEntrypointConfiguration

# original = KubeflowOrchestrator._configure_container_op

# def patch_container_op(container_op):
#     original(container_op)
#     container_op.container.add_env_variable(
#         k8s_client.V1EnvVar(name="ZENML_RUN_NAME", value="{{workflow.name}}")
#     )

# KubeflowOrchestrator._configure_container_op = staticmethod(patch_container_op)

# def patch_get_run_name(self, pipeline_name):
#     return os.getenv("ZENML_RUN_NAME")

# KubeflowEntrypointConfiguration.get_run_name = patch_get_run_name

####################################
####################################
####################################

# Configure warnings
warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)

# Specify docker configuration of pipeline
docker_config = DockerConfiguration(
    dockerfile="./docker_pipeline_parents/Dockerfile",
    build_context_root="./",
    requirements="./docker_pipeline_parents/requirements.txt",
)


@pipeline(docker_configuration=docker_config)
def training_pipeline(
    load_data,
    train_model,
    evaluate_model,
):

    load_dotenv()
    train_df, test_df = load_data()
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)

    return test_acc


if __name__ == "__main__":

    pipeline = training_pipeline(
        load_data=train_data_loader(),
        train_model=train_classifier(),
        evaluate_model=evaluate_classifier(),
    )
    pipeline.run()
