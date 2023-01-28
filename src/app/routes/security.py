import os
from typing import List

import numpy as np
import requests
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Security,
    UploadFile,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security.api_key import APIKey, APIKeyHeader
from sqlalchemy.orm import Session

from src.app.main import logger
from src.domain.class_mapping import class_mapping
from src.domain.data_preprocessing import preprocess_image_to_array
from src.io import crud, models, schemas
from src.io.mysql_database import SessionLocal, engine

router = APIRouter(prefix="/secured")
http_security = HTTPBasic()

API_KEY = os.environ.get("API_KEY")
API_KEY_NAME = os.environ.get("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# data structure creation in mysql
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Admin API security
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


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


@router.post("/users/", response_model=schemas.User, tags=["admin use"])
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    api_key_header: APIKey = Depends(get_api_key),
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User], tags=["admin use"])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key_header: APIKey = Depends(get_api_key),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User, tags=["admin use"])
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    api_key_header: APIKey = Depends(get_api_key),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/predict", status_code=200, tags=["basic use"])
async def predict(
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(http_security),
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
        tensor = preprocess_image_to_array(img)
        logger.info("File preprocessed.")
    except Exception as e:
        logger.error("Impossible to prepare input: {}".format(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse request body",
        )

    try:
        # Make the post request to model endpoint
        r = requests.post(
            url=os.environ.get("MODEL_PREDICT_ROUTE"),
            json={"instances": tensor.tolist()},
            # json={"instances": tensor.numpy().tolist()},
        )
    except Exception as e:
        logger.error("Impossible to make request to service: {}".format(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to make predictions",
        )

    label = np.argmax(r.json())
    logger.info("Predictions Ready.")

    return {"class label": str(class_mapping[label])}
