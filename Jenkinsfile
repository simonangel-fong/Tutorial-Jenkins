pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'Building...'
                sh 'pwd'
                sh 'docker build -t fastapi-app /var/lib/jenkins/workspace/docker-pipeline/module-pipeline-fastapi/fastapi-app/Dockerfile'
            }
        }
    }
}