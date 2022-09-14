pipeline {
    agent none
    stages {
        stage('Build & Push') {
            agent any
            steps {
                sh 'ls -l'
                sh 'docker build -t thomasbinder/ml_template:0.1 .'
                sh 'docker push thomasbinder/ml_template:0.1'
            }
        }
    }
}