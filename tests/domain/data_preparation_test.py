import tensorflow as tf

from src.domain.data_preparation import generate_data_for_training


def test_generate_data_for_training():

    # build params
    data_path = "./tests_data"
    batch_size = 1

    try:
        generate_data_for_training(data_path, batch_size)
        assert True
    except Exception as e:
        assert False
