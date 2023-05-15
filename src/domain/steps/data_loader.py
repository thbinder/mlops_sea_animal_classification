import os
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import tensorflow as tf
from google.cloud import storage
from sklearn.model_selection import train_test_split
from zenml.steps import BaseParameters, Output, step

from src.domain.class_mapping import class_mapping


class GoogleTrainDataLoderConfig(BaseParameters):
    """Google Data Loading params"""

    test_size: float = 0.2
    bucket_name: str = "sea-animals-data"
    project_id: str = "mlops-demos-376509"
    dl_dir: str = "/data"
    seed: int = 42


class LocalTrainDataLoderConfig(BaseParameters):
    """Local Training Data Loading params"""

    test_size: float = 0.2
    data_path: str = "./data"
    seed: int = 42


class LocalInferenceDataLoaderConfig(BaseParameters):
    """Local Inference Data Loading params"""

    target_shape: List[int] = [224, 224, 3]
    data_path: str = "./tests_data"


def load_data_from_folder(data_path, test_size, seed):
    """Loading and splitting data for training purposes"""

    image_dir = Path(data_path)
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
        image_df, test_size=test_size, shuffle=True, random_state=seed
    )

    print("Data prepared for training.")
    print("training data size: {}".format(train_df.size))
    print("validation data size: {}".format(test_df.size))
    print(train_df.head())

    return train_df, test_df


@step
def gcp_train_data_loader(
    config: GoogleTrainDataLoderConfig,
) -> Output(train_df=pd.DataFrame, test_df=pd.DataFrame):
    dl_dir = config.dl_dir
    storage_client = storage.Client(project=config.project_id)
    bucket = storage_client.get_bucket(config.bucket_name)

    print("Creating folders...")
    # Create folder for data if does not exist
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)
        print("{} folder created".format(dl_dir))
    # Retrieve raw data from every class
    print("Starting download.")
    for key in class_mapping:
        if not os.path.exists(dl_dir + "/" + class_mapping[key]):
            print("{} folder created".format(dl_dir + "/" + class_mapping[key]))
            os.makedirs(dl_dir + "/" + class_mapping[key])
        blobs = bucket.list_blobs(prefix=class_mapping[key])
        print("Downloading data for: {}.".format(class_mapping[key]))
        for blob in blobs:
            filename = blob.name.replace("/", "_")[len(class_mapping[key]) + 1 :]
            blob.download_to_filename(
                dl_dir + "/" + class_mapping[key] + "/" + filename
            )

    print("Download completed.")
    # Retrieve splitted data
    train_df, test_df = load_data_from_folder(
        config.dl_dir, config.test_size, config.seed
    )

    return train_df, test_df


@step
def local_train_data_loader(
    config: LocalTrainDataLoderConfig,
) -> Output(train_df=pd.DataFrame, test_df=pd.DataFrame):
    return load_data_from_folder(config.data_path, config.test_size, config.seed)


@step
def local_inference_data_loader(
    config: LocalInferenceDataLoaderConfig,
) -> np.ndarray:
    """Load some inference data."""

    def load_and_preprocess_image(img_path):
        buff = tf.io.read_file(img_path)
        buff = tf.io.decode_image(
            buff, channels=3, dtype=tf.dtypes.uint8, expand_animations=True
        )
        buff = tf.image.resize(buff, [224, 224])
        tensor = tf.reshape(buff, [1, 224, 224, 3])
        return tensor

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
