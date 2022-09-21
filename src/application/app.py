import logging

import cv2
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

MODEL = tf.keras.models.load_model("./exploration/model")

app = FastAPI()

class_mapping = {
    0: "Corals",
    1: "Crabs",
    2: "Dolphin",
    3: "Eel",
    4: "Jelly Fish",
    5: "Lobster",
    6: "Nudibranchs",
    7: "Octopus",
    8: "Penguin",
    9: "Puffers",
    10: "Sea Rays",
    11: "Sea Urchins",
    12: "Seahorse",
    13: "Seal",
    14: "Sharks",
    15: "Squid",
    16: "Starfish",
    17: "Turtle_Tortoise",
    18: "Whale",
}


@app.get("/ping")
async def ping():
    return {"message": "pong!"}


@app.post("/predict", status_code=200)
async def predict(file: UploadFile = File(...)):
    def resize(image):
        return cv2.resize(image, (224, 224))

    # Retrieve input file
    img = await file.read()
    logger.info("File received.")

    # Prepare Data
    try:
        img = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        img = resize(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img, dtype=np.float32).reshape(1, 224, 224, 3)
        logger.info("File pre processed.")
    except Exception as e:
        logger.error("Impossible to prepare input: {}".format(e))
        return {"status_code": 400, "error": "Unable to parse request body"}

    # Predict class
    try:
        preds = MODEL.predict(img)
        label = np.argmax(preds)
        logger.info("Predictions Ready.")
    except Exception as e:
        logger.error("Impossible to make predictions: {}".format(e))
        return {"status_code": 400, "error": "Unable to make predictions"}

    return {"class label": str(class_mapping[label])}
