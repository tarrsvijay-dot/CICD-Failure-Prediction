pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        VENV_PYTHON = '.venv\\Scripts\\python.exe'
    }

    stages {

        stage('Environment') {
            steps {
                echo '========================================'
                echo 'Checking Python environment'
                echo '========================================'

                bat '''
                    echo System Python:
                    "%PYTHON%" --version

                    echo.
                    echo Python executable:
                    "%PYTHON%" -c "import sys; print(sys.executable)"

                    echo.
                    echo Git:
                    git --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo '========================================'
                echo 'Creating Python virtual environment'
                echo '========================================'

                bat '''
                    if not exist ".venv\\Scripts\\python.exe" (
                        "%PYTHON%" -m venv .venv
                    )

                    "%VENV_PYTHON%" --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '========================================'
                echo 'Installing project dependencies'
                echo '========================================'

                bat '''
                    "%VENV_PYTHON%" -m pip install --upgrade pip
                    "%VENV_PYTHON%" -m pip install -r requirements.txt
                    "%VENV_PYTHON%" -m pip install -e .
                '''
            }
        }

        stage('Git Analysis') {
            steps {
                echo '========================================'
                echo 'Running Git Analysis'
                echo '========================================'

                bat '''
                    "%VENV_PYTHON%" src\\git_analyzer.py
                '''
            }
        }

        stage('CI/CD Check') {
            steps {
                echo '========================================'
                echo 'Running CI/CD Failure Prediction'
                echo '========================================'

                bat '''
                    .venv\\Scripts\\cicd.exe --check
                '''
            }
        }

        stage('Test') {
            steps {
                echo '========================================'
                echo 'Running Python validation'
                echo '========================================'

                bat '''
                    "%VENV_PYTHON%" -m py_compile src\\cicd_check.py
                    "%VENV_PYTHON%" -m py_compile src\\cicd_cli.py
                    "%VENV_PYTHON%" -m py_compile src\\git_analyzer.py
                    "%VENV_PYTHON%" -m py_compile src\\ci_predict.py
                    "%VENV_PYTHON%" -m py_compile src\\predict.py
                    "%VENV_PYTHON%" -m py_compile src\\predict_new.py

                    echo.
                    echo All selected Python files compiled successfully.
                '''
            }
        }

        stage('Pipeline Success') {
            steps {
                echo '========================================'
                echo '       CI/CD PIPELINE SUCCESS'
                echo '========================================'
                echo 'Python environment: OK'
                echo 'Dependencies: OK'
                echo 'Git analysis: OK'
                echo 'ML prediction: OK'
                echo 'Python validation: OK'
                echo '========================================'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline FAILED!'
            echo 'Check the failed stage in Console Output.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}