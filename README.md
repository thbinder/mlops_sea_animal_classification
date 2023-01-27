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

You shoud start by installing [PDM](https://github.com/pdm-project/pdm) the way you prefer. Afterwards, you can simply run the following command at the root of the project to setup your environment. It should spinup a project specific virtual environment with all the necessary packages.
```
pdm install
```

To try and run basic duties you can simply try out the following commands:
```
make help
```
This command will give you the list of jobs you can run with the Makefile, they should be self explanatory. They include starting unit testing, checking quality, running tests, coverage and cleaning your repo from temporary files.

### Run your first AI pipelines 🧠
-------------

Before running any pipeline you will need to do several things. First, set up (or reset) the default ZenML Stack and update it to use a the various components installed in the virtual environment.
```
./scripts/reset_zenml.sh
./infra/stacks/setup_local_stack.sh
```

Then you will need to retrieve the data, for this purpose you can use the ingestion notebook in the exploration folder. To make it work you'll need to have your kaggle credentials. Alternatively, you can just go to the website and download the data manually.

Once the stack is registered and the data ready, you can train & deploy your first model with ZenML & MLFlow !
```
./scripts/run_continuous_deployment_pipeline.sh
```

After the model is deployed, you can run an inference pipeline, it will load every image located in `./tests_data`, run the model on these and output the results.
```
./scripts/run_inference_pipeline.sh
```

To see your pipeline runs, you can deploy the zenml server and browse to its location.
```
zenml up
```

### Simple Docker API 🐳 
-------------

To distribute the model, one convenient way is to build the associated docker image with the model wrapped around a REST API. This can be done with the following command.
```
docker build -t <IMAGE_NAME> .
```

Afterwards, the docker image can be pushed to any repository, either manually or through continuous integration (cf Jenkins). The container and model can be tested locally by simply running the image and making the API calls through your browser.

```
docker run -p 8081:8081 <IMAGE_NAME>
```

Ideally, prior to pushing our image to a repository, we would like to ensure it passes integration tests. These tests and built & run by default if you use the continous integration jenkinsfile provided, but if you went the manual route, you would need to run them manually as well. To do this, you can simply run the following command and check the output.

```
cd ./tests_integration
./start.sh
```

### Docker Compose API Model Deployment 🐳
-------------

A more robust API can be deployed along with a MYSQL database holding information about authorized users. Prior to running the compose stack, you will need to fill the .env file with adapted parameters.

```
docker-compose up
```

Afterwards, the API should be accessible on port 8081.