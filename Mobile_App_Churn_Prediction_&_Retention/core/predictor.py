import pandas as pd
from prometheus_client import start_http_server, Summary
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
from scipy.stats import ks_2samp

MODEL_PREDICTION_LATENCY = Summary('model_prediction_latency_seconds', 'Time spent making a prediction')

class ChurnPredictor:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        start_http_server(8000)

    @MODEL_PREDICTION_LATENCY.time()
    def predict(self, user_features):
        user_scaled = self.scaler.transform([user_features])
        return int(self.model.predict(user_scaled)[0])

    def evaluate(self, y_true, y_pred):
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred)
        }

    def detect_drift(self, old_df, new_row):
        p_values = []
        for col in new_row.columns:
            ks, p = ks_2samp(old_df[col], new_row[col])
            p_values.append(p)
        return any(p < 0.05 for p in p_values)
