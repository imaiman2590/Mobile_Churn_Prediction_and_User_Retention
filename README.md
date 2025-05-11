 **Real-Time In-Memory Churn Prediction System**:

---

# 🔄 Real-Time In-Memory Churn Prediction System

A scalable, real-time churn prediction system powered by **Kafka**, **MSSQL**, and **in-memory machine learning models** (Random Forest, XGBoost, LSTM-GRU). This system eliminates `.pkl` and `joblib` files by keeping models in memory, making it ideal for long-running applications with real-time feedback loops.

## 🚀 Key Features

* **In-Memory Model Serving**: Models are trained and used directly in memory—no file I/O required.
* **Real-Time Data Ingestion**: Kafka pipelines simulate and consume user behavior data.
* **Live Prediction + Drift Detection**: Predict churn in real-time and automatically retrain models when drift is detected.
* **Predictive Feedback Loop**: Collect feedback via a FastAPI service and retrain periodically for improved accuracy.
* **Live Monitoring Dashboard**: Streamlit dashboard to visualize churn, user activity, and prediction trends.
* **Prometheus Integration**: Monitor model latency and performance using Prometheus metrics.

## 🧩 Architecture

```
Kafka Producer → Kafka Consumer → MSSQL → Model (in memory) → Predictions → Feedback API → Retrain Loop
```

Includes:

* Kafka + Zookeeper
* MSSQL Database
* Python services: Producer, Consumer, Predictor, Feedback API, Feedback Loop
* Streamlit Dashboard
* Prometheus monitoring
* Docker + Docker Compose orchestration

## 📦 Tech Stack

* Python 3.10
* Kafka & kafka-python
* MSSQL + pyodbc
* Scikit-learn, XGBoost, Keras (LSTM-GRU)
* Streamlit & Plotly
* FastAPI & Uvicorn
* Prometheus for monitoring

## ⚙️ How to Use

Clone the repo and spin up the entire stack using Docker:

```bash
docker-compose up --build
```

Navigate to:

* **Dashboard**: `http://localhost:8501`
* **Feedback API**: `http://localhost:8001/docs`
* **Prometheus**: `http://localhost:9090`

## 📁 Project Structure

```
churn-prediction/
├── producer.py            # Simulate user activity
├── consumer.py            # Consume Kafka messages to MSSQL
├── predictor.py           # In-memory churn prediction
├── train_model.py         # Model training logic
├── feedback_api.py        # REST API to submit user feedback
├── feedback_loop.py       # Periodic model retraining
├── dashboard/             # Streamlit UI
│   └── app.py
├── mssql_config.py        # MSSQL DB connection
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── prometheus.yml
```

## ✅ Highlights

* No model files—training and inference handled completely in RAM.
* Retraining is automatic when concept/feature drift is detected.
* Modular design supports rapid experimentation and scaling.

---

