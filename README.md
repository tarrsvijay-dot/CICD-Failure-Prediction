**CI/CD Pipeline Failure and Success Prediction using Machine Learning**

A Machine Learning-based system that predicts whether a CI/CD pipeline is likely to fail or succeed using historical software development and pipeline data.

**Project Overview**
CI/CD pipelines are essential for modern software development, but pipeline failures can slow down development and deployment.
This project uses Machine Learning and feature engineering to analyze historical commit and pipeline-related information and predict the likelihood of a pipeline failure or success.
The project includes a trained ML model, prediction scripts, and a Streamlit web application for interactive predictions.

**Objectives**
Predict CI/CD pipeline failure or success.
Analyze historical pipeline and commit data.
Engineer meaningful features from software development activity.
Train and evaluate Machine Learning models.
Provide an interactive prediction interface using Streamlit.
Integrate the prediction system with a CI/CD workflow.

**Machine Learning Features**
The model uses features related to software development and previous pipeline behavior, including:

Commit message length
Merge commit information
Number of parents
Code additions
Code deletions
Total code churn
Number of modified files
Time since previous commit
Previous pipeline failures
Previous pipeline runs
Previous failure rate
Recent failure count
Recent pipeline runs
Recent failure rate
Other historical and temporal features

....
These features help the model identify patterns associated with CI/CD pipeline failures.

**Project folder structure**
cicd-failure-prediction/
│
├── .github/
│   └── workflows/
│       └── ci-prediction.yml
│
├── models/
│   └── failure_model_v4.pkl
│
├── src/
│   ├── ci_predict.py
│   ├── create_run_target.py
│   ├── data_preprocessing.py
│   ├── evaluate_model.py
│   ├── evaluate_thresholds.py
│   ├── evaluate_v4_thresholds.py
│   ├── feature_engineering.py
│   ├── feature_engineering_v3.py
│   ├── inspect_dataset.py
│   ├── inspect_runs.py
│   ├── predict.py
│   ├── predict_new.py
│   ├── prepare_run_dataset.py
│   ├── train_model.py
│   ├── train_model_v2.py
│   ├── train_model_v3.py
│   ├── train_model_v4.py
│   └── train_time_based.py
│
├── app.py
├── requirements.txt
└── .gitignore

**Workflow**

Historical CI/CD Data
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Train / Test Split
        ↓
Machine Learning Model
        ↓
Model Evaluation
        ↓
Prediction
        ↓
Streamlit Application

**Technologies Used**
Python
Machine Learning
Scikit-learn
Pandas
NumPy
Streamlit
Git & GitHub
GitHub Actions
Pickle

**Dataset**
The project was developed using a large historical dataset containing software development and CI/CD-related information.
The raw and processed datasets are not stored in this repository because of their large size.
They are excluded using .gitignore.

**Model**
The final trained model is models/failure_model_v4.pkl
The project contains multiple versions of training and evaluation scripts developed during experimentation.
The V4 model represents the final model used by the application.

**Streamlit Application**
The project includes an interactive Streamlit application. 
Run it using streamlit run app.py

**Future Improvements**
Real-time integration with GitHub Actions
Automatic prediction for every pull request
Pipeline failure probability scoring
Automated notifications for high-risk pipelines
Model monitoring
Continuous model retraining
Cloud deployment
Integration with Jenkins, GitLab CI/CD, or other CI/CD platforms
More advanced Machine Learning models

**Author**
Tarrsan Vijay
M.Tech Software Engineering Student
VIT Vellore