pipeline {
    agent none
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'ls -l'
                sh 'docker build -t ml_template:0.1 .'
            }
        }
         stage('Push') {
            agent any
            steps {
                sh 'docker push thomasbinder/ml_template:0.1'
            }
        }
    }
}