# Sea Animals Classification

This projects aims to provide the basic skeleton for a well-configured ML work repository. It focuses on a simple computer vision problem of classifying some sea animals. 

🗃 Project Organization
------------

The `exploration` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process. This step is usually undertaken in the first stages of an AI project or while other routes (models, data preparation techniques and so on...) are being investigated.

The `src` folder should contain actual production code.
- `io`: should contain any I/O-related script: reading from and writing to S3 buckets, file conversions, reading a `.json` file. It covers interactions with the outside world.
- `domain`: contains all Python modules related to the internal workings of your code, like data cleaning, processing, formatting...This layer has no interaction with the outside world.
- `app`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `app` may contain several scripts like `app.py` which exposes a REST API to try out. The main function should be clear, concise and relay on methods defined on the `domain` directory.

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

### Run your first AI pipelines 🧠
-------------

You first need to deploy the necessary infrastructure services mentioned above. Then, set up (or reset) the default ZenML Stack and update it to use a the various services available.
```
./scripts/reset_zenml.sh
./stacks/setup_local_stack.sh
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

### Simple Docker API 🐳 
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

### Docker Compose API Model Deployment 🐳
-------------

A more robust API can be deployed along with a MYSQL database holding information about authorized users.

```
docker-compose up
```

Afterwards, the API should be accessible on port 8081.