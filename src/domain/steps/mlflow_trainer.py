from typing import List

import mlflow
import pandas as pd
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.steps import BaseParameters, Output, step

from src.domain.model import build_model


class TrainClassifierConfig(BaseParameters):
    """Trainer params"""

    validation_split: float = 0.2
    input_shape: List[int] = (224, 224, 3)
    dense_layers: List[int] = [256, 256, 19]
    dropout_layers: List[int] = [0.2, 0.2]
    batch_size: int = 4
    adam_param: float = 0.00001
    metrics: List[str] = ["accuracy"]
    loss: str = "categorical_crossentropy"
    nb_epochs: int = 2
    seed: int = 42
    allow_gpu: bool = False
    memory_limit: int = 0


@step(enable_cache=False, experiment_tracker="local_mlflow_tracker")
def train_classifier(
    config: TrainClassifierConfig,
    train_df: pd.DataFrame,
) -> Output(model=tf.keras.Model):

    # Check if GPU available
    print("GPUs Available: ", len(tf.config.list_physical_devices("GPU")))
    print("GPUs allowed: {}".format(config.allow_gpu))
    print("GPUS memory limit: {} MB".format(config.memory_limit))
    gpus = tf.config.list_physical_devices("GPU")

    if gpus:

        if not config.allow_gpu:
            print("GPUs not allowed for this run. Disabling...")
            try:
                # Disable first GPU
                tf.config.set_visible_devices(gpus[1:], "GPU")
                logical_devices = tf.config.list_logical_devices("GPU")
                # Logical device was not created for first GPU
                assert len(logical_devices) == len(gpus) - 1
                print("Tensorflow visible GPU: {}".format(len(logical_devices)))
            except Exception as e:
                # Invalid device or cannot modify virtual devices once initialized.
                print("Impossible to disable first GPU: {}".format(e))
                pass
        else:
            # Restrict TensorFlow to only allocate certain amount of memory on the first GPU
            print("GPUs allowed for this run. Setting memory limit...")
            try:
                tf.config.experimental.set_virtual_device_configuration(
                    gpus[0],
                    [
                        tf.config.experimental.VirtualDeviceConfiguration(
                            memory_limit=config.memory_limit
                        )
                    ],
                )
                logical_gpus = tf.config.experimental.list_logical_devices("GPU")
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except Exception as e:
                # Virtual devices must be set before GPUs have been initialized
                print("Impossible to set memory limit: {}".format(e))

    # Train data generator
    train_generator = ImageDataGenerator(validation_split=config.validation_split)
    # Split the data into train & validation categories.
    train_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        x_col="Filepath",
        y_col="Label",
        target_size=(config.input_shape[0], config.input_shape[1]),
        color_mode="rgb",
        class_mode="categorical",
        batch_size=config.batch_size,
        shuffle=True,
        seed=config.seed,
        subset="training",
    )

    val_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        x_col="Filepath",
        y_col="Label",
        target_size=(config.input_shape[0], config.input_shape[1]),
        color_mode="rgb",
        class_mode="categorical",
        batch_size=config.batch_size,
        shuffle=True,
        seed=config.seed,
        subset="validation",
    )

    # Build Model
    input_shape = (config.input_shape[0], config.input_shape[1], config.input_shape[2])
    model = build_model(input_shape, config.dense_layers, config.dropout_layers)
    # Compile training details
    model.compile(
        optimizer=tf.keras.optimizers.Adam(config.adam_param),
        loss=config.loss,
        metrics=config.metrics,
    )

    # Automatically log features
    mlflow.tensorflow.autolog()
    print("To observe run details in mlflow:")
    print("mlflow ui --backend-store-uri={} --port=4997".format(get_tracking_uri()))

    # Train Model
    model.fit(
        train_images,
        steps_per_epoch=len(train_images),
        validation_data=val_images,
        validation_steps=len(val_images),
        epochs=config.nb_epochs,
    )

    print("Model trained.")

    return model
