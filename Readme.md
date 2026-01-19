# 🚨 Disaster Victim Detection System

![Project Demo](PLACEHOLDER_FOR_YOUR_VIDEO_OR_GIF_LINK_HERE)

> **"Saving lives with AI."** > An automated computer vision system designed to detect victims in disaster zones (floods, earthquakes) using drone footage.

---

## 📖 Overview
This project leverages **Deep Learning (YOLOv8)** to identify humans in hazardous environments where manual rescue is difficult. It features a complete **End-to-End MLOps pipeline**, from data ingestion to deployment on **AWS Cloud** using **CI/CD**.

The system processes video inputs, detects victims with high precision, and renders the output with bounding boxes and confidence scores.

## ✨ Key Features
* **Object Detection:** Custom trained **YOLOv8** model specialized for aerial/drone imagery.
* **Web Application:** User-friendly interface built with **Flask** for uploading and analyzing videos.
* **Robust Video Processing:** Handles various video formats with automatic codec fallback (H.264/MP4V).
* **CI/CD Pipeline:** Fully automated deployment using **GitHub Actions**.
* **Cloud Native:** Dockerized application deployed on **AWS EC2** with images stored in **AWS ECR**.
* **Model Management:** Large model weights stored securely in **AWS S3**.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9
* **Frameworks:** Flask, PyTorch, Ultralytics YOLOv8
* **Computer Vision:** OpenCV (cv2)
* **DevOps:** Docker, GitHub Actions, AWS (EC2, ECR, S3, IAM)

---

## 👨‍💻 Development Workflow
If you want to contribute or add a new training/processing stage, follow this modular workflow:

1.  **Update `config/config.yaml`** (Define paths and constants)
2.  **Update `params.yaml`** (Model parameters like epochs, learning rate)
3.  **Update `entity`** (Define the return types for your functions in `src/victimDetector/entity`)
4.  **Update `ConfigurationManager`** (In `src/victimDetector/config/configuration.py`)
5.  **Update `Components`** (Write the actual logic in `src/victimDetector/components`)
6.  **Update `Pipeline`** (Orchestrate the component in `src/victimDetector/pipeline`)
7.  **Update `main.py`** (Add the pipeline execution trigger)
8.  **Update `dvc.yaml`** (Track the pipeline stage with DVC)

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.8+
* Docker (Optional)

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/prakash-saini69/disaster_victim_detection.git](https://github.com/prakash-saini69/disaster_victim_detection.git)
    cd disaster_victim_detection
    ```

2.  **Create a Conda Environment:**
    ```bash
    conda create -n victim_env python=3.8 -y
    conda activate victim_env
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    ```bash
    python app.py
    ```
    *Access the app at `http://localhost:8080`*

---

## ☁️ AWS CI/CD Deployment (Detailed Guide)

We use GitHub Actions for Continuous Deployment. Follow these steps to set up your own AWS environment.

### 1. Login to AWS Console

### 2. Create IAM User for Deployment
Create a new IAM user (e.g., `github-deployer`) with specific access permissions.

* **Permissions Required:**
    1.  `AmazonEC2FullAccess` (Virtual Machine access)
    2.  `AmazonEC2ContainerRegistryFullAccess` (Save Docker images)
    3.  `AmazonS3FullAccess` (Download trained model weights)

### 3. Create S3 Bucket (Model Storage)
* Create a bucket (e.g., `disaster-model-storage-2026`).
* **Upload your `model.pt` file here.**

### 4. Create ECR Repository
* Create a private repository named `disaster-victim-detection`.
* **Save the URI:** `123456789.dkr.ecr.us-east-1.amazonaws.com/disaster-victim-detection`

### 5. Create & Configure EC2 Machine
* **OS:** Ubuntu Server 22.04 or 24.04
* **Instance Type:** `t3.medium` or `m7i-flex.large` (Minimum 4GB RAM recommended for YOLO).
* **Security Group:** Open Port **8080** (Custom TCP) and **22** (SSH).

### 6. Install Docker on EC2
Connect to your EC2 instance via SSH and run these commands to install Docker:

```bash
# Optional: Update system
sudo apt-get update -y
sudo apt-get upgrade

# Required: Install Docker
curl -fsSL [https://get.docker.com](https://get.docker.com) -o get-docker.sh
sudo sh get-docker.sh

# Add permission to current user
sudo usermod -aG docker ubuntu
newgrp docker

Here is the updated, comprehensive README.md.

I have combined the professional project description with the detailed "How-to" guides for adding pipelines and setting up AWS CI/CD, exactly as you requested.

📝 README.md (Copy & Paste)
Markdown

# 🚨 Disaster Victim Detection System

![Project Demo](PLACEHOLDER_FOR_YOUR_VIDEO_OR_GIF_LINK_HERE)

> **"Saving lives with AI."** > An automated computer vision system designed to detect victims in disaster zones (floods, earthquakes) using drone footage.

---

## 📖 Overview
This project leverages **Deep Learning (YOLOv8)** to identify humans in hazardous environments where manual rescue is difficult. It features a complete **End-to-End MLOps pipeline**, from data ingestion to deployment on **AWS Cloud** using **CI/CD**.

The system processes video inputs, detects victims with high precision, and renders the output with bounding boxes and confidence scores.

## ✨ Key Features
* **Object Detection:** Custom trained **YOLOv8** model specialized for aerial/drone imagery.
* **Web Application:** User-friendly interface built with **Flask** for uploading and analyzing videos.
* **Robust Video Processing:** Handles various video formats with automatic codec fallback (H.264/MP4V).
* **CI/CD Pipeline:** Fully automated deployment using **GitHub Actions**.
* **Cloud Native:** Dockerized application deployed on **AWS EC2** with images stored in **AWS ECR**.
* **Model Management:** Large model weights stored securely in **AWS S3**.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9
* **Frameworks:** Flask, PyTorch, Ultralytics YOLOv8
* **Computer Vision:** OpenCV (cv2)
* **DevOps:** Docker, GitHub Actions, AWS (EC2, ECR, S3, IAM)

---

## 👨‍💻 Development Workflow
If you want to contribute or add a new training/processing stage, follow this modular workflow:

1.  **Update `config/config.yaml`** (Define paths and constants)
2.  **Update `params.yaml`** (Model parameters like epochs, learning rate)
3.  **Update `entity`** (Define the return types for your functions in `src/victimDetector/entity`)
4.  **Update `ConfigurationManager`** (In `src/victimDetector/config/configuration.py`)
5.  **Update `Components`** (Write the actual logic in `src/victimDetector/components`)
6.  **Update `Pipeline`** (Orchestrate the component in `src/victimDetector/pipeline`)
7.  **Update `main.py`** (Add the pipeline execution trigger)
8.  **Update `dvc.yaml`** (Track the pipeline stage with DVC)

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.8+
* Docker (Optional)

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/prakash-saini69/disaster_victim_detection.git](https://github.com/prakash-saini69/disaster_victim_detection.git)
    cd disaster_victim_detection
    ```

2.  **Create a Conda Environment:**
    ```bash
    conda create -n victim_env python=3.8 -y
    conda activate victim_env
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    ```bash
    python app.py
    ```
    *Access the app at `http://localhost:8080`*

---

## ☁️ AWS CI/CD Deployment (Detailed Guide)

We use GitHub Actions for Continuous Deployment. Follow these steps to set up your own AWS environment.

### 1. Login to AWS Console

### 2. Create IAM User for Deployment
Create a new IAM user (e.g., `github-deployer`) with specific access permissions.

* **Permissions Required:**
    1.  `AmazonEC2FullAccess` (Virtual Machine access)
    2.  `AmazonEC2ContainerRegistryFullAccess` (Save Docker images)
    3.  `AmazonS3FullAccess` (Download trained model weights)

### 3. Create S3 Bucket (Model Storage)
* Create a bucket (e.g., `disaster-model-storage-2026`).
* **Upload your `model.pt` file here.**

### 4. Create ECR Repository
* Create a private repository named `disaster-victim-detection`.
* **Save the URI:** `123456789.dkr.ecr.us-east-1.amazonaws.com/disaster-victim-detection`

### 5. Create & Configure EC2 Machine
* **OS:** Ubuntu Server 22.04 or 24.04
* **Instance Type:** `t3.medium` or `m7i-flex.large` (Minimum 4GB RAM recommended for YOLO).
* **Security Group:** Open Port **8080** (Custom TCP) and **22** (SSH).

### 6. Install Docker on EC2
Connect to your EC2 instance via SSH and run these commands to install Docker:

```bash
# Optional: Update system
sudo apt-get update -y
sudo apt-get upgrade

# Required: Install Docker
curl -fsSL [https://get.docker.com](https://get.docker.com) -o get-docker.sh
sudo sh get-docker.sh

# Add permission to current user
sudo usermod -aG docker ubuntu
newgrp docker
7. Configure EC2 as Self-Hosted Runner
Connect your EC2 instance to GitHub Actions so it can listen for code updates.

Go to GitHub Repo Settings > Actions > Runners > New self-hosted runner.

Choose Linux and run the provided commands in your EC2 terminal.

CRITICAL: Run the runner in the background using:

Bash

sudo ./svc.sh install
sudo ./svc.sh start



8. Setup GitHub Secrets
Go to Settings > Secrets and variables > Actions and add these keys:


Secret Name,Value Example
AWS_ACCESS_KEY_ID,AKIA... (From IAM Step)
AWS_SECRET_ACCESS_KEY,7cK9... (From IAM Step)
AWS_REGION,us-east-1
AWS_ECR_LOGIN_URI,123456789.dkr.ecr.us-east-1.amazonaws.com
ECR_REPOSITORY_NAME,disaster-victim-detection




👨‍💻 Author
Prakash Saini