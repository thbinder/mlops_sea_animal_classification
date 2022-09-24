from zenml.steps import BaseStepConfig, step


class DeploymentTriggerConfig(BaseStepConfig):
    """Deployment Trigger params"""

    seiling: float = 0.9


@step
def deployment_trigger(config: DeploymentTriggerConfig, test_acc: float) -> bool:
    """Only deploy if the global test accuracy > 50%."""
    return test_acc > config.seiling
