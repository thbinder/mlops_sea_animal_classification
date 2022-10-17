import logging
import os

import numpy as np
import requests
import tensorflow as tf
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.domain.class_mapping import class_mapping

# Configuration
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# App definition
app = FastAPI(
    title="Sea Animal Classification API",
    description="API for classifying sea animals.",
    version="0.1.0",
)
security = HTTPBasic()
user_db = {"thomas": "thomas"}


def verify_user(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password

    if not (user_db.get(username)) or not (user_db.get(username) == password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return


@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong!"}


@app.post("/v1/predict", status_code=200)
async def predict(
    file: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(security)
):
    """Returns the predicted class of an image"""

    # Verify credentials
    verify_user(credentials)

    # Retrieve input file
    img = await file.read()
    logger.info("File received.")

    # Prepare Data for prediction
    try:
        buff = tf.io.decode_image(
            img, channels=3, dtype=tf.dtypes.uint8, expand_animations=True
        )
        tensor = tf.image.resize(buff, [224, 224])
        tensor = tf.reshape(tensor, [1, 224, 224, 3])
    except Exception as e:
        logger.error("Impossible to prepare input: {}".format(e))
        return {"status_code": 400, "error": "Unable to parse request body"}

    try:
        r = requests.post(
            url="http://host.docker.internal:8000/invocations",
            json={"instances": tensor.numpy().tolist()},
        )
    except Exception as e:
        logger.error("Impossible to make request to service: {}".format(e))
        return {"status_code": 400, "error": "Unable to make request to service"}

    label = np.argmax(r.json())
    logger.info("Predictions Ready.")

    return {"class label": str(class_mapping[label])}
