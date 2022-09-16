# Jenkins deployment with Docker Compose
Simple to use deployment of an Jenkins Service based on [Jenkins BlueOcean](https://www.jenkins.io/doc/tutorials/create-a-pipeline-in-blue-ocean/)

## How to run

1. Build and run Jenkins Controller & Agent

    ```bash
    docker-compose up -d --build
    ```

2. Access Jenkins UI with http://localhost:8080