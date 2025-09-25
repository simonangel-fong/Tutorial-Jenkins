pipeline {
    agent { node { label 'docker_agent' } }
    stages {
        stage('test') {
            steps {
                sh '''
                whoami
                pwd
                uname -a
                '''
            }
        }
    }
}