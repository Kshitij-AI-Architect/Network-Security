# Network Security - Phishing Detection ML Pipeline

An end-to-end MLOps project for detecting phishing websites using machine learning. This project implements a complete ML pipeline with data ingestion from MongoDB, data validation, transformation, model training with hyperparameter tuning, and experiment tracking with MLflow/DagsHub.

## Project Overview

This system analyzes 30 different URL and website features to classify websites as legitimate or phishing. The pipeline is designed with production-ready practices including modular architecture, artifact management, and containerization.

## Features

- **MongoDB Integration**: Data storage and retrieval from MongoDB Atlas
- **Modular Pipeline Architecture**: Separate components for ingestion, validation, transformation, and training
- **Data Drift Detection**: Statistical tests (KS test) to detect distribution changes
- **Multiple ML Models**: Comparison of Random Forest, Decision Tree, Gradient Boosting, AdaBoost, and Logistic Regression
- **Hyperparameter Tuning**: GridSearchCV for optimal model parameters
- **Experiment Tracking**: MLflow integration with DagsHub for tracking metrics
- **CI/CD Pipeline**: Automated build, test, and deployment with GitHub Actions
- **AWS Deployment**: ECR for container registry, EC2 for hosting, S3 for model storage
- **Custom Exception Handling**: Detailed error tracking with file and line information
- **Logging**: Timestamped log files for debugging and monitoring
- **Docker Support**: Containerized deployment ready

## Project Structure

```
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py      # MongoDB data extraction & train-test split
│   │   ├── data_validation.py     # Schema validation & drift detection
│   │   ├── data_transformation.py # KNN imputation & preprocessing
│   │   └── model_trainer.py       # Model training & evaluation
│   ├── entity/
│   │   ├── config_entity.py       # Configuration classes
│   │   └── artifact_entity.py     # Artifact dataclasses
│   ├── constants/
│   │   └── training_pipeline/     # Pipeline constants & parameters
│   ├── utils/
│   │   ├── main_utils/            # YAML, pickle, numpy utilities
│   │   └── ml_utils/              # Model estimator & metrics
│   ├── exception/                 # Custom exception handling
│   └── logging/                   # Logger configuration
├── data_schema/
│   └── schema.yaml                # Data schema definition (31 features)
├── Network_Data/
│   └── phisingData.csv            # Raw phishing dataset
├── main.py                        # Pipeline orchestrator
├── push_data.py                   # MongoDB data loader
├── Dockerfile                     # Container configuration
├── requirements.txt               # Python dependencies
└── setup.py                       # Package setup
```

## ML Pipeline Stages

### 1. Data Ingestion
- Exports data from MongoDB collection to pandas DataFrame
- Saves raw data to feature store
- Performs 80-20 train-test split
- Outputs: `train.csv`, `test.csv`

### 2. Data Validation
- Validates column count against schema
- Detects data drift using Kolmogorov-Smirnov test
- Generates drift report in YAML format
- Outputs: Validated train/test files, drift report

### 3. Data Transformation
- Handles missing values using KNN Imputer (k=3)
- Transforms target labels (-1 → 0 for binary classification)
- Saves preprocessor object for inference
- Outputs: `.npy` arrays, `preprocessing.pkl`

### 4. Model Training
- Trains 5 different classifiers with GridSearchCV
- Evaluates using F1, Precision, and Recall scores
- Tracks experiments with MLflow
- Selects best model based on R² score
- Outputs: `model.pkl`, classification metrics

## Dataset Features

The model uses 30 features extracted from URLs and websites:

| Category | Features |
|----------|----------|
| URL-based | IP Address, URL Length, Shortening Service, @ Symbol, Double Slash, Prefix/Suffix, Subdomain |
| Domain-based | SSL State, Domain Registration Length, Age of Domain, DNS Record |
| Page-based | Favicon, HTTPS Token, Request URL, Anchor URLs, Links in Tags, SFH, iFrame |
| Behavior-based | Redirect, Mouse Over, Right Click, Popup Window |
| External | Web Traffic, Page Rank, Google Index, Links Pointing to Page |

**Target**: `Result` (1 = Legitimate, -1/0 = Phishing)

## Installation

```bash
# Clone the repository
git clone https://github.com/Kshitij-AI-Architect/Network-Security.git
cd Network-Security

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Configuration

Create a `.env` file in the root directory:

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
```

## Usage

### Load Data to MongoDB
```bash
python push_data.py
```

### Run Training Pipeline
```bash
python main.py
```

### Artifacts Output
Each run creates a timestamped folder in `Artifacts/`:
```
Artifacts/MM_DD_YYYY_HH_MM_SS/
├── data_ingestion/
│   ├── feature_store/
│   └── ingested/
├── data_validation/
│   ├── validated/
│   ├── invalid/
│   └── drift_report/
├── data_transformation/
│   ├── transformed/
│   └── transformed_object/
└── model_trainer/
    └── trained_model/
```

## CI/CD Pipeline

This project implements a complete CI/CD pipeline using GitHub Actions with AWS deployment.

### Pipeline Stages

```
Push to main branch
       ↓
┌─────────────────────────────────────┐
│  1. Continuous Integration          │
│     - Checkout code                 │
│     - Lint code                     │
│     - Run unit tests                │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  2. Continuous Delivery             │
│     - Configure AWS credentials     │
│     - Login to Amazon ECR           │
│     - Build Docker image            │
│     - Push image to ECR             │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  3. Continuous Deployment           │
│     - Pull latest image from ECR    │
│     - Run container on EC2          │
│     - Clean up old images           │
└─────────────────────────────────────┘
```

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | AWS region (e.g., us-east-1) |
| `AWS_ECR_LOGIN_URI` | ECR registry URI |
| `ECR_REPOSITORY_NAME` | ECR repository name |

## AWS Infrastructure

### Services Used

| Service | Purpose |
|---------|---------|
| **ECR** | Docker image registry for storing container images |
| **EC2** | Self-hosted runner for deployment & serving the application |
| **S3** | Model artifact storage for trained models |
| **IAM** | Access management with roles and policies |
| **App Runner** | Serverless container deployment (optional) |

### AWS Setup Steps

1. **Create IAM User** with programmatic access and attach policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonEC2FullAccess`
   - `AmazonS3FullAccess`

2. **Create ECR Repository**:
   ```bash
   aws ecr create-repository --repository-name networksecurity --region <your-region>
   ```

3. **Launch EC2 Instance**:
   - Ubuntu AMI
   - Install Docker
   - Configure as GitHub self-hosted runner

4. **Create S3 Bucket** for model storage:
   ```bash
   aws s3 mb s3://networksecurityai
   ```

### EC2 Runner Setup

```bash
# Install Docker on EC2
sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu
newgrp docker

# Configure as GitHub Actions self-hosted runner
# Follow GitHub Settings > Actions > Runners > New self-hosted runner
```

## Docker Deployment

### Local Deployment
```bash
# Build image
docker build -t network-security .

# Run container
docker run -d -p 8080:8080 --name networksecurity network-security
```

### AWS Deployment
The CI/CD pipeline automatically:
1. Builds the Docker image on push to `main`
2. Pushes to Amazon ECR
3. Deploys to EC2 via self-hosted runner

## Tech Stack

- **Python 3.10**
- **MongoDB** - Data storage
- **Scikit-learn** - ML models & preprocessing
- **MLflow + DagsHub** - Experiment tracking
- **FastAPI** - API serving
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **AWS ECR** - Container registry
- **AWS EC2** - Deployment & self-hosted runner
- **AWS S3** - Model artifact storage
- **AWS IAM** - Access management
- **Pandas/NumPy** - Data manipulation

