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
            steps {
                echo 'Deploying...'
                sh 'docker run --name fastapi-container -p 8001:8000 -d fastapi-app'
                sh 'firewall-cmd --permanent --add-port=8001/tcp'
                sh 'firewall-cmd --reload'
            }
        }
    }
}