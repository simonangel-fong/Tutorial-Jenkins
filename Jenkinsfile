pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'Building...'
                dir('/var/lib/jenkins/workspace/docker-pipeline/module-pipeline-fastapi/fastapi-app') {
                    sh 'pwd'
                    sh 'ls'
                    sh 'docker build -t fastapi-app .'
                }
            }
        }
    }
}