pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Git Analysis') {
            steps {
                bat 'python src\\git_analyzer.py'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline FAILED!'
        }
    }
}