from typing import List

import mlflow
import pandas as pd
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from zenml.steps import BaseParameters, Output, step


class EvaluateClassifierConfig(BaseParameters):
    """Trainer params"""

    input_shape: List[int] = (224, 224, 3)
    batch_size: int = 4


@step(enable_cache=False, experiment_tracker="mlflow_experiment_tracker")
def evaluate_classifier(
    config: EvaluateClassifierConfig, model: tf.keras.Model, test_df: pd.DataFrame
) -> Output(test_acc=float):

    # Test data generator
    test_generator = ImageDataGenerator()
    test_images = test_generator.flow_from_dataframe(
        dataframe=test_df,
        x_col="Filepath",
        y_col="Label",
        target_size=(config.input_shape[0], config.input_shape[1]),
        color_mode="rgb",
        class_mode="categorical",
        batch_size=config.batch_size,
        shuffle=False,
    )
    results = model.evaluate(test_images, verbose=1)
    mlflow.log_metric("Test accuracy", results[1])
    print("Model performance on Test Set:")
    print("Accuract on Test Set: {:.2f}".format(results[1]))

    return results[1]
