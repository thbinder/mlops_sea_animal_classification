from io import BytesIO

import numpy as np
from PIL import Image


def preprocess_image_to_array(data):
    """Prepares image data from buffer image for inference"""

    img = Image.open(BytesIO(data))
    img = img.resize((224, 224))
    array = np.array(img)

    return np.expand_dims(array, axis=0)


# def preprocess_image_to_tensor(img):

# """Prepares image data from buffer image for inference"""

# buff = tf.io.decode_image(
#     img, channels=3, dtype=tf.dtypes.uint8, expand_animations=True
# )
# tensor = tf.image.resize(buff, [224, 224])
# tensor = tf.reshape(tensor, [1, 224, 224, 3])

# return tensor
