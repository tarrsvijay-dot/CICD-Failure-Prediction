**CI/CD Failure Prediction using Machine Learning**
A machine learning-based system that analyzes Git commit and CI/CD pipeline characteristics to predict whether a software build is likely to succeed or fail. The project combines Machine Learning, Git analysis, Python, automated testing, and Jenkins CI/CD to demonstrate how historical development and commit-level information can be used for predictive analysis in software engineering.

**Project Overview**
CI/CD pipelines are essential for continuously building, testing, and delivering software. However, failed builds can waste development time and slow down software delivery.
This project attempts to predict CI/CD pipeline outcomes before or during the build process by analyzing features extracted from Git commits and historical pipeline data.

The system:
-> Extracts information from Git commits.
-> Processes and prepares the collected data.
-> Uses machine learning to predict pipeline success or failure.
-> Provides an application interface for prediction.
-> Runs automated tests.
-> Integrates the project with Jenkins for CI/CD automation.

**Key Features**
-> Git commit analysis
-> CI/CD failure and success prediction
-> Machine learning-based classification
-> Automated data processing
-> Model training and prediction
-> Python-based implementation
-> Automated unit testing with Pytest
-> Jenkins CI/CD integration
-> GitHub source-code management
-> Automated pipeline execution
-> Structured and modular project architecture

**Technology Stack**
Category	        Technology
Programming Language	Python
Machine Learning	Scikit-learn
Version Control       	Git
Repository	        GitHub
CI/CD	                Jenkins
Testing	                Pytest
Data Processing	        Pandas
Application	        Python
Environment	        Python Virtual Environment

**WorkFlow**
1. Git Commit Analysis

The system analyzes Git commits and extracts software-development-related features such as:

Commit hash
Number of parents
Merge commit information
Commit message length
Number of additions
Number of deletions
Total code churn

Example:

**CI/CD Git Analysis**
commit_hash: 666d4ae4cf35b691780a9a47de146fab5bb158d6
num_parents: 1
is_merge: 0
msg_len: 33
additions: 1
deletions: 1
total_churn: 2

These features can then be used as inputs to the machine learning pipeline.

2. Data Processing

The collected information is transformed into a structured dataset suitable for machine learning.

The preprocessing stage prepares the features and target values required for model training and evaluation.

3. Machine Learning

A classification model is trained using historical CI/CD data.

The model learns relationships between development/commit characteristics and pipeline outcomes.

The target prediction is:

SUCCESS
   or
FAILURE
4. Prediction

After training, the model can receive relevant input features and estimate whether the corresponding CI/CD execution is likely to succeed or fail.

5. Automated Testing

The project contains automated tests using Pytest to verify that important components behave as expected.

Tests can be executed using:

pytest
6. Jenkins CI/CD Integration

The project uses a Jenkinsfile to automate the CI/CD workflow.

A typical pipeline performs tasks such as:

GitHub Repository
       │
       ▼
   Jenkins
       │
       ▼
Checkout Source Code
       │
       ▼
Setup Python Environment
       │
       ▼
Install Dependencies
       │
       ▼
Run Tests
       │
       ▼
Run Application / ML Pipeline
       │
       ▼
Build Result

Jenkins can monitor the GitHub repository and automatically trigger a pipeline when changes are detected.


**Running the Project Locally**
1. Clone the Repository
git clone https://github.com/tarrsvijay-dot/CICD-Failure-Prediction.git
cd CICD-Failure-Prediction
2. Create a Virtual Environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Tests
pytest
5. Run the Application
python app.py
Jenkins Pipeline

The project contains a Jenkinsfile that defines the automated CI/CD workflow.

Jenkins can be configured to:

Connect to the GitHub repository
Detect repository changes
Checkout the latest source code
Configure the Python environment
Install project dependencies
Execute automated tests
Run the machine learning application
Report the build status

This demonstrates the integration of Machine Learning + Git + GitHub + Jenkins + Automated Testing within a single software engineering project.

**Machine Learning Workflow**

Historical CI/CD Data
        │
        ▼
Data Collection
        │
        ▼
Data Preprocessing
        │
        ▼
Feature Engineering
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Trained Model
        │
        ▼
New CI/CD Features
        │
        ▼
Prediction
        │
        ▼
 ┌───────────────┐
 │ SUCCESS/FAILURE│
 └───────────────┘


**Testing**

Automated testing is included to improve reliability and detect problems before deployment.

Run:

pytest

A successful test execution indicates that the tested project components are functioning correctly.

DevOps Integration

This project demonstrates a complete development-to-automation workflow:

Developer
   │
   ▼
Git
   │
   ▼
GitHub
   │
   ▼
Jenkins
   │
   ├── Checkout
   ├── Install Dependencies
   ├── Test
   ├── Execute
   └── Report
          │
          ▼
     Build Result
          │
          ▼
 Machine Learning
 Prediction
Objectives

The main objectives of this project are:

Build a machine learning system for CI/CD failure prediction.
Analyze Git commit characteristics.
Automate software testing.
Integrate machine learning with DevOps practices.
Implement a Jenkins-based CI/CD pipeline.
Demonstrate practical use of predictive analytics in software engineering.
Understand how development activity can be used to identify potential pipeline failures.
Future Improvements

Possible future improvements include:

Collecting a larger real-world CI/CD dataset.
Adding more Git and pipeline features.
Comparing multiple machine learning algorithms.
Improving model accuracy and evaluation.
Adding real-time Jenkins build data.
Integrating Jenkins APIs for automated prediction.
Adding model monitoring.
Deploying the prediction service to the cloud.
Creating dashboards for CI/CD failure trends.
Integrating AWS or Azure services.
Implementing continuous model retraining.
Project Status

Status: Completed — Core ML and CI/CD pipeline implementation

The project currently includes Git analysis, machine learning components, automated testing, project configuration, and Jenkins CI/CD integration.

**Author**
**Tarrsan Vijay
Software Engineering Student
VIT Vellore**
