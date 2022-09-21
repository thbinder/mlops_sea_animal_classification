import os
from pathlib import Path

import pandas as pd
from keras_preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split


def generate_data_for_training(data_path, batch_size):

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
        image_df, test_size=0.2, shuffle=True, random_state=42
    )

    # Train data generator
    train_generator = ImageDataGenerator(validation_split=0.2)
    # Test data generator
    test_generator = ImageDataGenerator()

    # Split the data into three categories.
    train_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        x_col="Filepath",
        y_col="Label",
        target_size=(224, 224),
        color_mode="rgb",
        class_mode="categorical",
        batch_size=batch_size,
        shuffle=True,
        seed=42,
        subset="training",
    )

    val_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        x_col="Filepath",
        y_col="Label",
        target_size=(224, 224),
        color_mode="rgb",
        class_mode="categorical",
        batch_size=batch_size,
        shuffle=True,
        seed=42,
        subset="validation",
    )

    test_images = test_generator.flow_from_dataframe(
        dataframe=test_df,
        x_col="Filepath",
        y_col="Label",
        target_size=(224, 224),
        color_mode="rgb",
        class_mode="categorical",
        batch_size=batch_size,
        shuffle=False,
    )

    return train_images, val_images, test_images, test_df
