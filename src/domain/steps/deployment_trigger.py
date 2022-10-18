from zenml.steps import BaseParameters, step


class DeploymentTriggerConfig(BaseParameters):
    """Deployment Trigger params"""

    seiling: float = 0.9


@step(enable_cache=False)
def deployment_trigger(config: DeploymentTriggerConfig, test_acc: float) -> bool:
    """Only deploy if the global test accuracy > seiling."""

    if test_acc > config.seiling:
        print("Newly trained model performances is above threshold.")
        print("Deployment accepted.")

    return test_acc > config.seiling
