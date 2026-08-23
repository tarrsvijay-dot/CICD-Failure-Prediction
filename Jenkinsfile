pipeline {

    agent any

    stages {

        stage('Checkout') {

            steps {
                checkout scm
            }
        }


        stage('Check Python') {

            steps {

                bat '''
                    python --version
                    pip --version
                '''
            }
        }


        stage('Install Dependencies') {

            steps {

                bat '''
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pip install -e .
                '''
            }
        }


        stage('CI/CD Risk Check') {

            steps {

                bat '''
                    cicd --check
                '''
            }
        }
    }
}