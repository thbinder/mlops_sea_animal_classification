# Machine Learning Project Template

This projects aims to provide the basic skeleton for a well-configured work repository. It focuses on a simple computer vision problem of classifying a few sea animals. 

## Getting started with this template

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

💻 MLFlow (local)
-------------

Build and launch mlflow local server from the infra folder. For more information refer to the related readme.
```
cd infra/mlflow
docker-compose up -d --build
```

💻 Jenkins (local)
-------------

Build and launch jenkins local server from the infra folder. For more information refer to the related readme.
```
cd infra/jenkins
docker-compose up -d --build
```

You can then safely navigate to localhost:8080 to connect to your Jenkins deployment and setup your pipeline if it wasn't previously configured. If you are having a plugin issue, just navigate to localhost:8080/restart.

To make the current Jenkinsfile work, you will need to create a set of credentials for your registry. We use DockerHub for conveniance and an associated access token for Jenkins [used through the Credentials Plugin](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/injecting-secrets).

Once the pipeline has been setup correctly (providing credentials & git repository) you can build the project and create github actions.

🤖 ZenML Stack (local)
-------------

Set Up (or reset) the default ZenML Stack, then update it to use a local mlflow server as experiment tracker and model deployer, as well as evidently as data validator. You will need to fill in the mlflow username & password you set up for your mlflow deployment. If you used the docker-compose file from this repository, you can leave it blank.
```
./scripts/reset_zenml.sh
./scripts/register_local_stack.sh
```
Run a first training pipeline
```
./scripts/run_training_pipeline.sh
```
Train & deploy with MLFlow your first model
```
./scripts/run_continuous_training_pipeline.sh
```
Run an inference pipeline, loading every images located in `./tests_data`
```
./scripts/run_inference_pipeline.sh
```

🐳 Kubeflow Orchestrator (local)
-------------

Ensure you deployed Kubeflow pipelines, refer to infra/kubeflow. Afterwards, you can simply register and update the right stack components, then run your training script. ZenML will dynamically look for the local Dockerfile and use it as basis for the pipeline environment to be sent to Kubeflow.
```
pdm export -o infra/zenml/requirements.txt --without-hashes
./scripts/update_kubeflow_stack.sh
./scripts/run_kubeflow_training_pipeline.sh
```

🐳 Docker API Model Deployment (local)
-------------

Build and Run Docker image
```
docker build -t <IMAGE_NAME> .
docker run -p 8000:8000 <IMAGE_NAME>
```

🗃 Project Organization
------------

The `exploration` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process.

The `src` folder should contain actual production code.
- `io`: should contain any I/O-related script: reading from and writing to S3 buckets, file conversions, reading a `.json` file. It covers interactions with the outside world.
- `domain`: contains all Python modules related to the internal workings of your code, like data cleaning, processing, formatting...This layer has no interaction with the outside world.
- `api`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `api` may contain several scripts like `app.py` which exposes a REST API to try out. The main function should be clear, concise and relay on methods defined on the `domain` directory.