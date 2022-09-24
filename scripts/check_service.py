import cv2
import numpy as np
from zenml.repository import Repository

repo = Repository()
model_deployer = repo.active_stack.model_deployer
services = model_deployer.find_model_server(
    pipeline_name="training_pipeline",
    pipeline_step_name="mlflow_model_deployer_step",
    running=True,
)
service = services[0]

if service.check_status():

    # just the model is served, therefore preprocessing needs to be handled
    img = cv2.imread('./test_data/nudibranch.jpg', 0)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.array(img, dtype=np.float32).reshape(1, 224, 224, 3)
    pred = service.predict(img)
    print(pred)

else:
    print("Service not running")
    print("Run: pdm run zenml model-deployer models list")
    print("Verify the model is deployed")