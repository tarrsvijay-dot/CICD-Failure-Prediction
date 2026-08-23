pipeline {

    agent any

    environment {
        PYTHON = 'C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        PYTHON_SCRIPTS = 'C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\Scripts'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '''
                    "%PYTHON%" --version
                    "%PYTHON%" -m pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    "%PYTHON%" -m pip install -r requirements.txt
                    "%PYTHON%" -m pip install -e .
                '''
            }
        }

        stage('CI/CD Risk Check') {
            steps {
                bat '''
                    set "PATH=%PYTHON_SCRIPTS%;%PATH%"
                    cicd --check
                '''
            }
        }
    }
}