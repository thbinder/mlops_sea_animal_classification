import os
import warnings
from cgitb import enable
from pathlib import Path
from typing import List

import mlflow
import pandas as pd
import tensorflow as tf
from absl import logging as absl_logging
from dotenv import load_dotenv
from keras_preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from zenml.integrations.mlflow.mlflow_step_decorator import enable_mlflow
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step
from zenml.pipelines import pipeline
from zenml.steps import BaseStepConfig, Output, step

from src.domain.model import build_model

warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)


class ImageDataLoderSetConfig(BaseStepConfig):
    """Data Loading params"""

    test_size: float = 0.2
    data_path: str = "./data"
    seed: int = 42


class TrainClassifierSetConfig(BaseStepConfig):
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


class DeploymentTriggerConfig(BaseStepConfig):
    """Deployment Trigger params"""

    seiling: float = 0.9


@step
def image_data_loader(
    config: ImageDataLoderSetConfig,
) -> Output(train_df=pd.DataFrame, test_df=pd.DataFrame):

    image_dir = Path(config.data_path)
    # Get filepaths and labels
    filepaths = (
        list(image_dir.glob(r"**/*.JPG"))
        + list(image_dir.glob(r"**/*.jpg"))
        + list(image_dir.glob(r"**/*.png"))
        + list(image_dir.glob(r"**/*.PNG"))
    )
    labels = list(map(lambda x: os.path.split(os.path.split(x)[0])[1], filepaths))
    filepaths = pd.Series(filepaths, name="Filepath").astype(str)
    labels = pd.Series(labels, name="Label")
    # Concatenate filepaths and labels
    image_df = pd.concat([filepaths, labels], axis=1)

    # Separate in train and test data
    train_df, test_df = train_test_split(
        image_df, test_size=config.test_size, shuffle=True, random_state=config.seed
    )

    return train_df, test_df


@enable_mlflow
@step
def train_classifier(
    config: TrainClassifierSetConfig,
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


@enable_mlflow
@step
def evaluate_classifier(
    config: TrainClassifierSetConfig, model: tf.keras.Model, test_df: pd.DataFrame
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
    mlflow.log_metric("Test accuracy", results[1] * 100)

    return results[1] * 100


@step
def deployment_trigger(config: DeploymentTriggerConfig, test_acc: float) -> bool:
    """Only deploy if the global test accuracy > 50%."""
    return test_acc > config.seiling


@pipeline
def training_pipeline(
    load_data,
    train_model,
    evaluate_model,
    deployment_trigger=deployment_trigger(),
    model_deployer=mlflow_model_deployer_step(),
):

    load_dotenv()
    train_df, test_df = load_data()
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)
    deployment_decision = deployment_trigger(test_acc)
    model_deployer(deployment_decision, model)

    return test_acc
