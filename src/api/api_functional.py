import logging
import os
from typing import List

import numpy as np
import requests
import tensorflow as tf
from fastapi import Depends, FastAPI, File, HTTPException, Security, UploadFile, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security.api_key import APIKey, APIKeyHeader
from sqlalchemy.orm import Session

from src.data import crud, models, schemas
from src.data.mysql_database import SessionLocal, engine
from src.domain.class_mapping import class_mapping

API_KEY = os.environ.get("API_KEY")
API_KEY_NAME = os.environ.get("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# data structure creation in mysql
models.Base.metadata.create_all(bind=engine)

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User API security
def verify_user(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    """Checks if user is granted access to the API"""

    username = credentials.username
    password = credentials.password

    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=400, detail="Username not registered")

    user_password = crud.get_user_password(db, username=username)
    if user_password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return


# Admin API security
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


@app.post("/users/", response_model=schemas.User, tags=["admin use"])
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    api_key_header: APIKey = Depends(get_api_key),
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User], tags=["admin use"])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key_header: APIKey = Depends(get_api_key),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["admin use"])
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    api_key_header: APIKey = Depends(get_api_key),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/ping", status_code=200, tags=["basic use"])
async def ping():
    """Returns message if API is alive and healthy"""
    return {"message": "pong!"}


@app.post("/v1/predict", status_code=200, tags=["basic use"])
async def predict(
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Returns the predicted class of an image"""

    # Verify credentials
    verify_user(credentials, db)

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
            # TODO: make an argument of url
            url=os.environ.get("MODEL_PREDICT_ROUTE"),
            json={"instances": tensor.numpy().tolist()},
        )
    except Exception as e:
        logger.error("Impossible to make request to service: {}".format(e))
        return {"status_code": 400, "error": "Unable to make request to service"}

    label = np.argmax(r.json())
    logger.info("Predictions Ready.")

    return {"class label": str(class_mapping[label])}
