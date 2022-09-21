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

To make the current Jenkinsfile work, you will need to create a set of credentials for your registry. Here we use DockerHub and an associated access token for Jenkins [used through the Credentials Plugin](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/injecting-secrets).

🐳 Deployment (local)
-------------

Build and Run Docker image
```
docker build -t <IMAGE_NAME> .
docker run <IMAGE_NAME> -p 8080:127.0.0.1:8080
```

🗃 Project Organization
------------

The `notebooks` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process. I have added an example which leverages the features of an mlflow server. You can setup your own in whichever way you like and change the tracking uri so that the notebook sends data to the correct location.

The `src` folder should contain actual production code.
- `data`: should contain any I/O-related script: reading from and writing to S3 buckets, file conversions, reading a `.json` file. It covers interactions with the outside world.
- `env`: should contain your configuration script(s) that read environement variable and turns them into Python global variables across your whole package.
- `domain`: contains all Python modules related to the internal workings of your code, like data cleaning, processing, formatting...This layer has no interaction with the outside world.
- `application`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `application` may contain several scripts like `train.py`, `predict.py`. The main function should be clear, concise and relay on methods defined on the `domain` directory.
