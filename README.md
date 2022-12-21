# Sea Animals Classification

This projects aims to provide the basic skeleton for a well-configured ML work repository. It focuses on a simple computer vision problem of classifying some sea animals. 

🗃 Project Organization
------------

The `exploration` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process. This step is usually undertaken in the first stages of an AI project or while other routes (models, data preparation techniques and so on...) are being investigated.

The `src` folder should contain actual production code.
- `data`: should contain any I/O-related script: reading from and writing to S3 buckets, file conversions, reading a `.json` file. It covers interactions with the outside world.
- `domain`: contains all Python modules related to the internal workings of your code, like data cleaning, processing, formatting...This layer has no interaction with the outside world.
- `api`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `api` may contain several scripts like `app.py` which exposes a REST API to try out. The main function should be clear, concise and relay on methods defined on the `domain` directory.

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

### Setting development infrastructure 💻
-------------

Build and launch the different services locally from the infra folder. For more information on the services, refer to the related readmes.
```
cd infra/<SERVICE_NAME>
docker-compose up -d --build
```

List of available local infrastructure 
- MLFlow will be deployed on localhost:5000. (Required to run exploration notebooks)
- Minio will be deployed on localhost:9000. (Required to run exploration notebooks)
- Vault will be deployed on localhost:8200. (Only needed for ZenML local stack)
- Jenkins will be deployed on localhost:8080. (Only required for Continuous Integration from the git repo)

### Run your first AI pipelines 🧠
-------------

You first need to deploy the necessary infrastructure services mentioned above. Then, set up (or reset) the default ZenML Stack and update it to use a the various services available.
```
./scripts/reset_zenml.sh
./scripts/register_local_stack.sh
```
Once the stack is registered, you can train & deploy your first model with ZenML & MLFlow !
```
./scripts/run_continuous_deployment_pipeline.sh
```

After the model is deployed, you can run an inference pipeline, it will load every image located in `./tests_data`, run the model on these and output the results.
```
./scripts/run_inference_pipeline.sh
```

Alternatively, to access the model and to mimic a setup closer to production grade, you can deploy a functional API that will forward your requests directly to the MLFLow deployed model. (See src/api/api_functional.py). 
```
docker run --add-host host.docker.internal:host-gateway -p 8081:8081 api_functional:0.1
```

To see your pipeline runs, you can deploy the zenml server and browse to its location.
```
zenml up --docker
```

### Docker API 🐳 
-------------

To distribute the model one convenient way is to build the associated docker image with the model wrapped around a REST API. This can be done with the following command.
```
docker build -t <IMAGE_NAME> .
```

Afterwards, the docker image can be pushed to any repository, either manually or through continuous integration (cf Jenkins). The container and model can be tested locally by simply running the image and making the API calls through your browser.

```
docker run -p 8000:8000 <IMAGE_NAME>
```

Ideally, prior to pushing our image to a repository, we would like to ensure it passes integration tests. These tests and built & run by default if you use the continous integration jenkinsfile provided, but if you went the manual route, you would need to run them manually as well. To do this, you can simply run the following command and check the output.

```
cd ./tests_integration
./start.sh
```

### Minikube API Model Deployment 🐳
-------------

A more robust way to deploy your model is through a kubernetes cluster. In this example, we'll assume you have minikube installed and setup locally as well as the previous docker image built and pushed to a repository accessible to your minikube deployment. In this example, we have used DockerHub.

Simply run the setup.sh script in the kubernetes infra folder, it should spin up minikube and create the necessary resources. Don't forget to change de name of the images if need be.
```
./setup.sh
```

Afterwards, your service should be accessible through your minikube deployment. The console will output the address on which you can access the web UI.