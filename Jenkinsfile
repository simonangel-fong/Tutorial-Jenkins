pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'Building...'
                sh 'pwd'
                sh 'docker build -t fastapi-app ./module-pipeline-fastapi/fastapi-app/Dockerfile'
            }
        }
    }
}