import logging
import os

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile

from src.domain.class_mapping import class_mapping

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

MODEL = tf.keras.models.load_model("./model")
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong!"}


@app.post("/predict", status_code=200)
async def predict(file: UploadFile = File(...)):

    # Retrieve input file
    img = await file.read()
    logger.info("File received.")

    # Prepare Data
    try:
        buff = tf.io.decode_image(
            img, channels=3, dtype=tf.dtypes.uint8, expand_animations=True
        )
        tensor = tf.image.resize(buff, [224, 224])
        tensor = tf.reshape(tensor, [1, 224, 224, 3])
    except Exception as e:
        logger.error("Impossible to prepare input: {}".format(e))
        return {"status_code": 400, "error": "Unable to parse request body"}

    # Predict class
    try:
        preds = MODEL.predict(tensor)
        label = np.argmax(preds)
        logger.info("Predictions Ready.")
    except Exception as e:
        logger.error("Impossible to make predictions: {}".format(e))
        return {"status_code": 400, "error": "Unable to make predictions"}

    return {"class label": str(class_mapping[label])}
