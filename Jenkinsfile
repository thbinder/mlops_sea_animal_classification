pipeline {
    agent none
    stages {
        stage('Test') {
            agent any
            steps {
                sh 'ls -l'
                sh 'make test'
            }
        }
        stage('Build') {
            agent any
            steps {
                sh 'ls -l'
                sh 'docker build -t thomasbinder/sea_animals_api:0.1 .'
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