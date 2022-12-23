import logging
import os

import numpy as np
import tensorflow as tf
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.domain.class_mapping import class_mapping
from src.domain.data_preprocessing import preprocess_image_to_tensor

# Loading ML model
MODEL = tf.keras.models.load_model("./model")

# Logging Configuration
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
http_security = HTTPBasic()

# If deployment with mysql database
if os.environ.get("MYSQL_CONNECTION") == "YES":
    from .routes import security

    app.include_router(security.router)


@app.get("/ping", status_code=200, tags=["basic use"])
async def ping():
    """Returns message if API is alive and healthy"""
    return {"message": "pong!"}


@app.post("/predict", status_code=200, tags=["test use"])
async def predict(
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(http_security),
):
    """Returns the predicted class of an image"""

    ### Check dummy credentials
    if credentials.username != "thomas" or credentials.password != "thomas":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Retrieve input file
    img = await file.read()
    logger.info("File received.")

    # Prepare Data for prediction
    try:
        tensor = preprocess_image_to_tensor(img)
    except Exception as e:
        logger.error("Impossible to prepare input: {}".format(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse request body",
        )

    # Predict class of image
    try:
        preds = MODEL.predict(tensor)
        label = np.argmax(preds)
        logger.info("Predictions Ready.")
    except Exception as e:
        logger.error("Impossible to make predictions: {}".format(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to make predictions",
        )

    return {"class label": str(class_mapping[label])}
