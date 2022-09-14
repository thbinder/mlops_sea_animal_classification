pipeline {
    agent none
    stages {
        stage('Docker Build') {
            agent any
            steps {
                sh 'docker build -t ml_template:latest .'
            }
        }
    }
}