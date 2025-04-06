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
                    sh 'docker rm fastapi-container'
                    sh 'docker run --name fastapi-container -p 8001:8000 -d fastapi-app'
                }
            }
        }
        // stage('test') {
        //     steps {
        //         echo '...'
        //         dir('/var/lib/jenkins/workspace/docker-pipeline/module-pipeline-fastapi/fastapi-app') {
        //             sh 'docker exec fastapi-container '
        //         }
        //     }
        // }
    }
}