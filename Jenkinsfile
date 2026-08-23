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
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '========================================'
                echo 'Installing Python dependencies'
                echo '========================================'

                bat '''
                    "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m pip install --upgrade pip

                    if exist requirements.txt (
                        "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m pip install -r requirements.txt
                    ) else (
                        echo WARNING: requirements.txt not found
                    )
                '''
            }
        }

        stage('Run Git Analyzer') {
            steps {
                echo '========================================'
                echo 'Running Git Analyzer'
                echo '========================================'

                bat '''
                    if exist src\\git_analyzer.py (
                        "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" src\\git_analyzer.py
                    ) else (
                        echo ERROR: src\\git_analyzer.py not found
                        exit /b 1
                    )
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
                        "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m py_compile src\\predict.py
                    ) else (
                        echo WARNING: src\\predict.py not found
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
                        "C:\\Users\\tarrs\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m py_compile src\\train_model_v4.py
                    ) else (
                        echo WARNING: src\\train_model_v4.py not found
                    )
                '''
            }
        }

        stage('Pipeline Success') {
            steps {
                echo '========================================'
                echo 'CI/CD PIPELINE PASSED'
                echo '========================================'
                echo 'All validation stages completed successfully.'
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