pipeline {
    agent none
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'ls -l'
                sh 'docker build -t thomasbinder/sea_animals_api:0.1 .'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'docker/compose:latest'
                    args '--privileged'
                }
            }
            steps {
                sh 'docker version'
                sh 'docker-compose version'
                sh 'cd ./tests_integration/ && ls -l && ./start.sh'
            }
        }
        stage('Push') {
            agent any
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_secret_key', passwordVariable: 'password', usernameVariable: 'username')]) {
                    sh 'docker login -u $username -p $password'
                }
                sh 'docker push thomasbinder/sea_animals_api:0.1'
            }
        }
    }
}