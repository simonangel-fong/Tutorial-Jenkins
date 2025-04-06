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
    post {
        failure {
            mail to: 'simonangelfong@gmail.com',
                 subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The tests failed in ${env.JOB_NAME} build #${env.BUILD_NUMBER}. Check Jenkins for details: ${env.BUILD_URL}"
        }
        success {
            mail to: 'simonangelfong@gmail.com',
                 subject: "Build Succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The build and tests passed for ${env.JOB_NAME} build #${env.BUILD_NUMBER}. App deployed successfully! Check Jenkins: ${env.BUILD_URL}"
        }
    }
}