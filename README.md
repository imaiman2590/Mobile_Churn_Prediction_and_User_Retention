

---

````markdown
# 🧠 Real-Time In-Memory Churn Prediction System

A real-time, fully in-memory machine learning system for churn prediction using Kafka, MSSQL, FastAPI, and Streamlit. Designed to support real-time predictions and feedback-based retraining without relying on disk-based model serialization (`.pkl` or `joblib`).

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
````

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Launch All Services

```bash
docker-compose up --build
```

### 3️⃣ Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🔧 Configuration

### MSSQL (`mssql_config.py`)

```python
def get_mssql_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;PORT=1433;DATABASE=retention_db;'
        'UID=your_username;PWD=your_password'
    )
```

---

## 📦 Tech Stack

* Python (scikit-learn, XGBoost, TensorFlow/Keras)
* Kafka & Zookeeper
* FastAPI + Uvicorn
* Streamlit + Plotly
* MSSQL
* Prometheus
* Docker + Docker Compose

---

## 📈 Monitoring

* Prometheus scrapes `/metrics` from the predictor service.
* Example metric: `model_prediction_latency_seconds`

To run Prometheus:

```bash
docker-compose up prometheus
```

---

## ✅ Use Cases

* SaaS or gaming user churn prediction
* Real-time user behavior modeling
* Feedback-driven model improvement pipelines

---



---

## 🤝 Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/my-feature`)
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License.

```

---

Let me know if you'd like me to include GitHub badges (e.g., build status, license) or generate a preview for how it will look on GitHub.
```
