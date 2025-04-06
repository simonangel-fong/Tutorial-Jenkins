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
            mail(
                body: 'This email was sent by a test Jenkins Pipeline job, using Gmail SMTP.', 
                subject: 'Jenkins Pipeline job email', 
                to: 'tech.arguswatcher@gmail.com')
        }
        success {
            mail(
                body: 'This email was sent by a test Jenkins Pipeline job, using Gmail SMTP.', 
                subject: 'Jenkins Pipeline job email', 
                to: 'tech.arguswatcher@gmail.com'
            )
        }
    }
}