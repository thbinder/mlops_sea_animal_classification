import numpy as np
from zenml.services import BaseService
from zenml.steps import Output, step

from src.domain.class_mapping import class_mapping


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

    print(results)
    return results
