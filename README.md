# Machine Learning Project Template

This projects aims to provide the basic skeleton for a well-configured work repository. Each time you start a new project, please make a copy of this structure in your own repository to gain time and work better, harder, faster and stronger 🤖


## Getting started with this template
Create an empty GitHub repository for your new projet. 
Then you can use this following lines to start a new project:

```
cd <NEW_PROJECT_NAME>
./scripts/setup.sh
```

The setup script will ensure pipx and pdm are installed with your current python version. Then, it will run the command pdm install which basically sets you up for working with the repo. Then, you can complete the information about your project and delete all the previous lines within the pyproject.toml. At least change name, description and authors.

To run basic duties locally you can simply try out the following commands:
```
make help
```
This command will give you the list of jobs you can run with the Makefile, they should be self explanatory. For example,

```
make check-types
```
Will check that types are correctly being used throughout the project. Other provided duties include checking quality, running tests, coverage and cleaning your repo from temporary files.

💻  Run Jenkins Pipeline (local)
-------------

Build blueocean Jenkins Docker images.
```
docker pull jenkins/jenkins
docker pull docker:dind
docker network create jenkins
```

Run first docker image (docker in docker)
```
docker run \
  --name jenkins-docker \
  --rm \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind \
  --storage-driver overlay2
```

Build and start jenkins image
```
cd infra/jenkins/
docker build -t myjenkins-blueocean:2.346.3-1 .
docker run \
  --name jenkins-blueocean \
  --restart=on-failure \
  --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:2.346.3-1
```

Run docker logs to retrieve Jenkins token
```
docker logs jenkins-blueocean
```

You can then safely navigate to localhost:8080 to connect to your Jenkins deployment. If you are having a plugin issue, just navigate to localhost:8080/restart.

💻  Installation (local)
-------------

Build of Docker image
```
docker build -t <IMAGE_NAME> .
```


🐳 Run Docker image
------------

Run a Docker image
```
docker run <IMAGE_NAME> -p 8080:127.0.0.1:8080
```


🗃 Project Organization
------------

The `notebooks` folder contains the different visualisation and experimentation notebooks that can be needed during the exploration process.

The `src` folder contains your actual code. You will see 4 directories within the `src` folder:
- `data`: should contain any I/O-related script, for instance reading from and writing to S3 buckets, file conversions, reading a `.json` file. In a sense, see `data` as your code interaction with the outside world.
- `env`: should contain your configuration script(s) that read environement variable such as the (uncommitted) `.env` file and turns them into Python global variables across your whole package.
- `domain`: contains all Python scripts related to the internal workings of your code, like data cleaning, processing, formatting,...This layer has no interaction with the outside world
- `application`: contains your main code functions, for example the `main.py` script if your code as a sole purpose. In the case of an ML project repository, `application` may contain several scripts like `train.py`, `predict.py`. The main function should be clear, concise and relay on methods defined on the `domain` directory.
