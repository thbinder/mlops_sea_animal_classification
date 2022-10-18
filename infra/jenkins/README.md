# Jenkins deployment with Docker Compose
Simple to use deployment of an Jenkins Service based on [Jenkins BlueOcean](https://www.jenkins.io/doc/tutorials/create-a-pipeline-in-blue-ocean/)

## How to run

1. Build and run Jenkins Controller & Agent

    ```bash
    docker-compose up -d --build
    ```

2. Access Jenkins UI with http://localhost:8080

3. Credentials

    To make the current Jenkinsfile work, you will need to create a set of credentials for your registry. We use DockerHub for conveniance and an associated access token for Jenkins [used through the Credentials Plugin](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/injecting-secrets).

    Once the pipeline has been setup correctly (providing credentials & git repository) you can build the project from jenkins and create github actions.