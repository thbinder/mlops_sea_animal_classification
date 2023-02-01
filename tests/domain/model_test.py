import tensorflow as tf

from src.domain.model import build_model


def test_build_model():
    # build params
    input_shape = (200, 200, 3)
    denses = [10, 10, 10]
    dropout = [0.2, 0.2]

    # associated input param
    x = tf.ones((1, 200, 200, 3))

    model = build_model(input_shape, denses, dropout)
    y = model(x)

    assert y.shape == [1, 10]
