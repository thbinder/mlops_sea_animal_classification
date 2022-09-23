from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, Dropout, Input, Lambda
from tensorflow.keras.models import Sequential


def build_model(input_shape, denses, dropout):
    before_mobilenet = Sequential(
        [
            Input(shape=input_shape),
            Lambda(preprocess_input),
        ]
    )

    mobilenet = MobileNetV2(
        input_shape=input_shape, include_top=False, weights="imagenet", pooling="avg"
    )
    mobilenet.trainable = False

    after_mobilenet = Sequential(
        [
            Dense(denses[0], activation="relu"),
            Dropout(dropout[0]),
            Dense(denses[1], activation="relu"),
            Dropout(dropout[1]),
            Dense(denses[2], activation="softmax"),
        ]
    )

    model = Sequential([before_mobilenet, mobilenet, after_mobilenet])

    return model
