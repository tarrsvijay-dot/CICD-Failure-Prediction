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
                    echo Python location:
                    where python

                    echo.
                    echo Python version:
                    python --version

                    echo.
                    echo Python executable:
                    python -c "import sys; print(sys.executable)"
                '''
            }
        }

        stage('Check Project Structure') {
            steps {
                echo '========================================'
                echo 'Checking project structure'
                echo '========================================'

                bat '''
                    echo Current directory:
                    cd

                    echo.
                    echo Project files:
                    dir

                    echo.
                    echo Source files:
                    dir src
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '========================================'
                echo 'Installing Python dependencies'
                echo '========================================'

                bat '''
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Git Analyzer') {
            steps {
                echo '========================================'
                echo 'Running Git Analyzer'
                echo '========================================'

                bat '''
                    python src\\git_analyzer.py
                '''
            }
        }

        stage('Validate Prediction Code') {
            steps {
                echo '========================================'
                echo 'Checking prediction scripts'
                echo '========================================'

                bat '''
                    python -m py_compile src\\predict.py
                    python -m py_compile src\\predict_new.py
                    python -m py_compile src\\ci_predict.py

                    echo.
                    echo Prediction scripts compiled successfully.
                '''
            }
        }

        stage('Validate ML Scripts') {
            steps {
                echo '========================================'
                echo 'Checking ML scripts'
                echo '========================================'

                bat '''
                    python -m py_compile src\\feature_engineering.py
                    python -m py_compile src\\feature_engineering_v3.py
                    python -m py_compile src\\data_preprocessing.py
                    python -m py_compile src\\train_model.py
                    python -m py_compile src\\train_model_v2.py
                    python -m py_compile src\\train_model_v3.py
                    python -m py_compile src\\train_model_v4.py
                    python -m py_compile src\\evaluate_model.py

                    echo.
                    echo ML scripts compiled successfully.
                '''
            }
        }

        stage('Pipeline Success') {
            steps {
                echo '========================================'
                echo '       CI/CD PIPELINE SUCCESS'
                echo '========================================'
                echo 'Python environment verified.'
                echo 'Dependencies installed.'
                echo 'Git analyzer executed.'
                echo 'Prediction code validated.'
                echo 'ML scripts validated.'
                echo '========================================'
            }
        }
    }

    post {

        success {
            echo 'Jenkins build completed successfully!'
        }

        failure {
            echo 'Jenkins build FAILED.'
            echo 'Check the Console Output for the failing stage.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}