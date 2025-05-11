# 🧠 Real-Time In-Memory Churn Prediction System

A machine learning system for churn prediction using Kafka, MSSQL, FastAPI, and Streamlit. Designed to support real-time predictions and feedback-based retraining without relying on disk-based model serialization (`.pkl` or `joblib`).

---

## 🔍 Features

### ✅ In-Memory ML Pipeline
- Models are trained once at runtime and kept in memory.
- Supports RandomForest, XGBoost, and LSTM-GRU models.
- Retrains models periodically using feedback data—no file-based model loading.

### 🔄 Feedback Loop
- FastAPI-based feedback API for submitting actual churn results.
- Periodic retraining integrates new data for improved predictions.

### 📡 Kafka Streaming
- Kafka producer generates user activity events.
- Kafka consumer ingests data into MSSQL for feature generation.

### 📊 Streamlit Dashboard
- Real-time visualization of churn predictions and activity logs.
- KPI metrics, prediction trends, and feature monitoring.

### 📈 Prometheus Monitoring
- Tracks model latency and performance via Prometheus.
- Easy to integrate with Grafana for full observability.

---

## 📁 Project Structure

```bash
churn-prediction/
├── producer.py           # Kafka producer for user events
├── consumer.py           # Kafka consumer writing to MSSQL
├── predictor.py          # Churn predictor with in-memory model
├── train_model.py        # Model training script
├── feedback_api.py       # API to collect user feedback
├── feedback_loop.py      # Periodic model retraining
├── dashboard/
│   └── app.py            # Real-time Streamlit dashboard
├── mssql_config.py       # MSSQL connection config
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker build file
├── docker-compose.yml    # Docker service orchestration
└── prometheus.yml        # Prometheus scraping config
