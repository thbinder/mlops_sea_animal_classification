import os
from pathlib import Path
from typing import List

import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from zenml.steps import BaseStepConfig, Output, step

from src.domain.model import build_model


class TrainDataLoderConfig(BaseStepConfig):
    """Data Loading params"""

    test_size: float = 0.2
    data_path: str = "./data"
    seed: int = 42


class InferenceDataLoaderConfig(BaseStepConfig):
    """Data Loading params"""

    target_shape: List[int] = [224, 224, 3]
    data_path: str = "./test_data"


@step
def train_data_loader(
    config: TrainDataLoderConfig,
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


@step
def inference_data_loader(
    config: InferenceDataLoaderConfig,
) -> np.ndarray:
    """Load some inference data."""

    def load_and_preprocess_image(img_path):
        img = cv2.imread(img_path, 0)
        img = cv2.resize(img, (config.target_shape[0], config.target_shape[1]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img, dtype=np.float32).reshape(
            1, config.target_shape[0], config.target_shape[1], config.target_shape[2]
        )
        return img

    data_dir = Path(config.data_path)
    filepaths = (
        list(data_dir.glob(r"**/*.JPG"))
        + list(data_dir.glob(r"**/*.jpg"))
        + list(data_dir.glob(r"**/*.png"))
        + list(data_dir.glob(r"**/*.PNG"))
    )

    print("Inference pipeline will run on the following images:")
    print(filepaths)

    first_image_flag = True
    for img_path in filepaths:

        img_path = str(img_path)
        if first_image_flag:
            imgs_array = load_and_preprocess_image(img_path)
            first_image_flag = False
        else:
            img = load_and_preprocess_image(img_path)
            imgs_array = np.concatenate((imgs_array, img), axis=0)

    return imgs_array
