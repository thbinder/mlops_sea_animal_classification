from typing import List

import mlflow
import pandas as pd
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from zenml.integrations.mlflow.mlflow_step_decorator import enable_mlflow
from zenml.steps import BaseStepConfig, Output, step

from src.domain.model import build_model


class TrainClassifierConfig(BaseStepConfig):
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


@enable_mlflow
@step
def train_classifier(
    config: TrainClassifierConfig,
    train_df: pd.DataFrame,
) -> Output(model=tf.keras.Model):

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
    # Train Model
    model.fit(
        train_images,
        steps_per_epoch=len(train_images),
        validation_data=val_images,
        validation_steps=len(val_images),
        epochs=config.nb_epochs,
    )

    return model
