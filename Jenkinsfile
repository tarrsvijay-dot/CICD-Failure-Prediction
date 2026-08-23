pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '========================================'
                echo 'Checking out project from GitHub'
                echo '========================================'

                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                echo '========================================'
                echo 'Checking Python installation'
                echo '========================================'

                bat '''
                    echo Python version:
                    "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" --version

                    echo.
                    echo Python executable:
                    "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -c "import sys; print(sys.executable)"
                '''
            }
        }

        stage('Check Project Structure') {
            steps {
                echo '========================================'
                echo 'Checking project structure'
                echo '========================================'

                bat '''
                    dir

                    echo.
                    echo Checking important files...

                    if exist src (
                        echo src folder found
                    ) else (
                        echo ERROR: src folder not found
                        exit /b 1
                    )

                    if exist app.py (
                        echo app.py found
                    ) else (
                        echo WARNING: app.py not found
                    )

                    if exist requirements.txt (
                        echo requirements.txt found
                    ) else (
                        echo ERROR: requirements.txt not found
                        exit /b 1
                    )
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
                        "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv .venv
                    )

                    ".venv\\Scripts\\python.exe" --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '========================================'
                echo 'Installing Python dependencies'
                echo '========================================'

                bat '''
                    ".venv\\Scripts\\python.exe" -m pip install --upgrade pip

                    ".venv\\Scripts\\python.exe" -m pip install -r requirements.txt

                    ".venv\\Scripts\\python.exe" -m pip install -e .
                '''
            }
        }

        stage('Run Git Analyzer') {
            steps {
                echo '========================================'
                echo 'Running Git Analysis'
                echo '========================================'

                bat '''
                    if exist src\\git_analyzer.py (
                        ".venv\\Scripts\\python.exe" src\\git_analyzer.py
                    ) else (
                        echo ERROR: src\\git_analyzer.py not found
                        exit /b 1
                    )
                '''
            }
        }

        stage('CI/CD Failure Prediction') {
            steps {
                echo '========================================'
                echo 'Running CI/CD Failure Prediction'
                echo '========================================'

                bat '''
                    ".venv\\Scripts\\cicd.exe" --check
                '''
            }
        }

        stage('Validate Prediction Code') {
            steps {
                echo '========================================'
                echo 'Validating Prediction Code'
                echo '========================================'

                bat '''
                    if exist src\\predict.py (
                        ".venv\\Scripts\\python.exe" -m py_compile src\\predict.py
                    )

                    if exist src\\predict_new.py (
                        ".venv\\Scripts\\python.exe" -m py_compile src\\predict_new.py
                    )
                '''
            }
        }

        stage('Validate ML Scripts') {
            steps {
                echo '========================================'
                echo 'Validating ML Scripts'
                echo '========================================'

                bat '''
                    if exist src\\train_model_v4.py (
                        ".venv\\Scripts\\python.exe" -m py_compile src\\train_model_v4.py
                    )

                    if exist src\\ci_predict.py (
                        ".venv\\Scripts\\python.exe" -m py_compile src\\ci_predict.py
                    )

                    if exist src\\cicd_check.py (
                        ".venv\\Scripts\\python.exe" -m py_compile src\\cicd_check.py
                    )

                    if exist src\\cicd_cli.py (
                        ".venv\\Scripts\\python.exe" -m py_compile src\\cicd_cli.py
                    )

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
        always {
            echo 'Jenkins pipeline execution finished.'
        }

        success {
            echo 'Jenkins build SUCCESS.'
        }

        failure {
            echo 'Jenkins build FAILED.'
            echo 'Check the Console Output for the failing stage.'
        }
    }
}