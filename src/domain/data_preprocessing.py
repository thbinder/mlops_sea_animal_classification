import tensorflow as tf

def preprocess_image_to_tensor(img):

    """Prepares image data from buffer image for inference"""

    buff = tf.io.decode_image(
        img, channels=3, dtype=tf.dtypes.uint8, expand_animations=True
    )
    tensor = tf.image.resize(buff, [224, 224])
    tensor = tf.reshape(tensor, [1, 224, 224, 3])

    return tensor