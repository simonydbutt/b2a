pipeline {
    agent none
    stages {
        stage('Run') {
            agent {
                docker {
                    image 'python:3.6-alpine'
                }
            }
            steps {
                sh 'cd /b2b/'
                sh 'pip3 install -r requirements.txt'
                sh 'python Trigger.sh'
            }
        }
    }
}