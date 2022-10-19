# Sea Animals Classification

This projects aims to provide the basic skeleton for a well-configured ML work repository. It focuses on a simple computer vision problem of classifying a few sea animals. 

## Getting started

You can use this following lines to start a new project:
```
./scripts/setup.sh
```
The setup script will ensure pipx and pdm are installed with your current python version. Then, it will run the command pdm install which basically sets you up for working with the repo. Alternatively, you can install [PDM](https://github.com/pdm-project/pdm) the way you prefer. 

Namely, if you have installed pdm with pipx, you can simply run the following command at the root of the project to setup your environment:
```
python3.8 -m pipx run pdm install
```

To run basic duties locally you can simply try out the following commands:
```
make help
```
This command will give you the list of jobs you can run with the Makefile, they should be self explanatory. They include starting unit testing, checking quality, running tests, coverage and cleaning your repo from temporary files.

💻 MLFlow | MinIO | Jenkins | Vault (local)
-------------

Build and launch the different services locally from the infra folder. For more information on the services, refer to the related readmes.
```
cd infra/<SERVICE_NAME>
docker-compose up -d --build
```

MLFlow will be deployed on localhost:5000. (Required to run exploration notebooks)
Minio will be deployed on localhost:9000. (Required to run exploration notebooks)
Jenkins will be deployed on localhost:8080. If you are having a plugin issue, just navigate to localhost:8080/restart. (Required for Continuous Integration)
Vault will be deployed on localhost:8200 and is only needed if you plan on using the ZenML local stack.

🐳 Docker API Model Deployment (local)
-------------

Build and Run Docker image
```
docker build -t <IMAGE_NAME> .
docker run -p 8000:8000 <IMAGE_NAME>
```

Alternatively, if you ran a CI pipeline with jenkins, such as the one provided in this project, you can simply pull the image from your repository and run it.

🐳 Minikube API Model Deployment (local)
-------------

Build and push the docker image Docker image to a registry accessible to your minikube deployment.
```
docker build -t <IMAGE_NAME> .
docker push <IMAGE_NAME>
```
Run the setup.sh script in the kubernetes infra folder, it should spin up minikube and create the necessary resources. Don't forget to change de name of the images if need be.
```
./setup.sh
```

Afterwards, your service should be accessible through your minikube deployment.

🤖 ZenML Stack (local)
-------------

Set Up (or reset) the default ZenML Stack, then update it to use a local mlflow server as experiment tracker and model deployer, as well as evidently as data validator. Different stacks are available from the scripts folder. However, most of them need a prior deployment of the service needed, such as MLFow, MinIO and Vault.
```
./scripts/reset_zenml.sh
./scripts/register_local_stack.sh
```
Train & deploy your first model with MLFlow
```
./scripts/run_continuous_deployment_pipeline.sh
```
Run an inference pipeline, loading every images located in `./tests_data`
```
./scripts/run_inference_pipeline.sh
```

Alternatively to running an inference pipeline, you can deploy a functional API that will forward your requests directly to the deployed model. (See src/api/api_functional.py). 
```
docker run --add-host host.docker.internal:host-gateway -p 8081:8081 api_functional:0.1
```

To see your pipeline runs, you can deploy the zenml server and browse to its location.
```
zenml up --docker
```

🗃 Project Organization
------------

The `exploration` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process.

The `src` folder should contain actual production code.
- `data`: should contain any I/O-related script: reading from and writing to S3 buckets, file conversions, reading a `.json` file. It covers interactions with the outside world.
- `domain`: contains all Python modules related to the internal workings of your code, like data cleaning, processing, formatting...This layer has no interaction with the outside world.
- `api`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `api` may contain several scripts like `app.py` which exposes a REST API to try out. The main function should be clear, concise and relay on methods defined on the `domain` directory.