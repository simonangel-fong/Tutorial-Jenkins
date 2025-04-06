pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'Building...'
                dir('/var/lib/jenkins/workspace/docker-pipeline/module-pipeline-fastapi/fastapi-app') {
                    sh 'docker build -t fastapi-app .'
                }
            }
        }
        stage('test') {
            steps {
                echo 'Testing...'
                sh 'docker run --rm fastapi-app pytest'
            }
        }
        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh 'docker stop fastapi-app || exit 0'
                sh 'docker rm fastapi-app || exit 0'
                sh 'docker run -d --name fastapi-app -p 8000:8000 fastapi-app'
            }
        }
    }
}