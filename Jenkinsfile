pipeline {
    agent none
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'echo current directory'
                sh 'ls -l'
                sh 'docker build -t ml_template:latest .'
            }
        }
    }
}