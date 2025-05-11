from config.mssql_config import get_mssql_connection
from core.model_trainer import generate_features, train_model
import pandas as pd

def retrain_model():
    conn = get_mssql_connection()
    activity = pd.read_sql("SELECT * FROM user_activity", conn)
    feedback = pd.read_sql("SELECT * FROM churn_feedback", conn)

    user_stats = generate_features(activity)
    merged = pd.merge(user_stats, feedback, on='user_id')
    X = merged[['total_activity_days', 'session_count', 'days_since_last', 'avg_session_length']]
    y = merged['true_churn'].astype(int)

    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=200, max_depth=10)
    model.fit(X_scaled, y)

    return model, scaler
