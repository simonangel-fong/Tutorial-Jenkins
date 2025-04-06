pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'Building...'
                sh 'pwd'
                sh 'cd ./module-pipeline-fastapi/fastapi-app/'
                sh 'ls'
                sh 'docker build -t fastapi-app .'
            }
        }
    }
}