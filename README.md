# Machine Learning Project Template

This projects aims to provide the basic skeleton for a well-configured work repository. Each time you start a new project, one can copy this structure to gain time and work better, harder, faster and stronger 🤖

## Getting started with this template

You can use this following lines to start a new project:
```
./scripts/setup.sh
```
The setup script will ensure pipx and pdm are installed with your current python version. Then, it will run the command pdm install which basically sets you up for working with the repo. Then, you can complete the information about your project and delete all the previous lines within the pyproject.toml. At least change name, description and authors... 

Alternatively, you can install [PDM](https://github.com/pdm-project/pdm) the way you prefer.

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

🐳 ZenML Stack (local)
-------------

Set Up (or reset) the default ZenML Stack, then update it to use a local mlflow server as experiment tracker and model deployer, as well as evidently as data validator. You will need to fill in the mlflow username & password you set up for your mlflow deployment. If you used the docker-compose file from this repository, you can leave it blank.
```
./scripts/reset_zenml.sh
./scripts/register_update_local_stack.sh
```
Run a first training pipeline
```
./scripts/run_training_pipeline.sh
```
Train & deploy with MLFlow your first model
```
./scripts/run_train_continuous_deployment_pipeline.sh
```
Run an inference pipeline, loading every images located in `./test_data`
```
./scripts/run_inference_pipeline.sh
```

🐳 Docker API Model Deployment (local)
-------------

Build and Run Docker image
```
docker build -t <IMAGE_NAME> .
docker run <IMAGE_NAME> -p 8080:127.0.0.1:8080
```

🗃 Project Organization
------------

The `exploration` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process. I have added an example which leverages the features of an mlflow server. You can setup your own in whichever way you like and change the tracking uri so that the notebook sends data to the correct location.

The `src` folder should contain actual production code.
- `io`: should contain any I/O-related script: reading from and writing to S3 buckets, file conversions, reading a `.json` file. It covers interactions with the outside world.
- `domain`: contains all Python modules related to the internal workings of your code, like data cleaning, processing, formatting...This layer has no interaction with the outside world.
- `api`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `api` may contain several scripts like `app.py` which exposes a REST API to try out. The main function should be clear, concise and relay on methods defined on the `domain` directory.