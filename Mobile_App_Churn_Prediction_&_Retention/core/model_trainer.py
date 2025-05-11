import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from scipy.stats import randint

from mssql_config import get_mssql_connection

def train_model():
    # Fetch data from MSSQL
    conn = get_mssql_connection()
    df = pd.read_sql("SELECT * FROM user_activity", conn)

    # Feature engineering
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    user_stats = df.groupby('user_id').agg(
        total_activity_days=('timestamp', lambda x: x.dt.date.nunique()),
        last_seen=('timestamp', 'max'),
        session_count=('action', 'count')
    ).reset_index()

    user_stats['days_since_last'] = (pd.Timestamp.now() - user_stats['last_seen']).dt.days
    user_stats['avg_session_length'] = user_stats['session_count'] // user_stats['total_activity_days']
    user_stats['churned'] = user_stats['days_since_last'] > 7

    X = user_stats[['total_activity_days', 'session_count', 'days_since_last', 'avg_session_length']]
    y = user_stats['churned'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

X_train_scaled = X_train_scaled.reshape((X_train_scaled.shape[0]X_train_scaled.shape[1]))  # Add 1 timestep
X_test_scaled = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))  # Add 1 timestep

# Step 6: Define the LSTM-GRU Model
lstm_gru_model = Sequential()

# Add LSTM layer
lstm_gru_model.add(LSTM(64, input_shape=(X_train_scaled.shape[1], X_train_scaled.shape[2]), activation='relu', return_sequences=True))

# Add GRU layer
lstm_gru_model.add(GRU(32, activation='relu'))

# Dropout for regularization
lstm_gru_model.add(Dropout(0.5))

# Dense layer for churn prediction (binary output: churn or not churn)
lstm_gru_model.add(Dense(1, activation='sigmoid'))

# Compile the model
lstm_gru_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model with early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
lstm_gru_model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test), callbacks=[early_stopping])

# Step 7: Evaluate the LSTM-GRU Model
lstm_gru_accuracy = lstm_gru_model.evaluate(X_test_scaled, y_test)[1]
print(f"LSTM-GRU Model Accuracy: {lstm_gru_accuracy}")

    # Hyperparameter tuning for RandomForest and XGBoost
    rf_params = {
        'n_estimators': randint(100, 500),
        'max_depth': randint(5, 15),
        'min_samples_split': randint(2, 10),
        'min_samples_leaf': randint(1, 10)
    }

    xgb_params = {
        'n_estimators': randint(100, 500),
        'max_depth': randint(3, 10),
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.7, 0.8, 0.9],
        'colsample_bytree': [0.7, 0.8, 0.9]
    }

    rf_search = RandomizedSearchCV(RandomForestClassifier(), rf_params, n_iter=10, cv=5, random_state=42)
    xgb_search = RandomizedSearchCV(XGBClassifier(), xgb_params, n_iter=10, cv=5, random_state=42)

    rf_search.fit(X_train_scaled, y_train)
    xgb_search.fit(X_train_scaled, y_train)

    best_rf = rf_search.best_estimator_
    best_xgb = xgb_search.best_estimator_

    # Evaluate models
    rf_score = best_rf.score(X_test_scaled, y_test)
    xgb_score = best_xgb.score(X_test_scaled, y_test)

    print(f"Best Random Forest Model Accuracy: {rf_score}")
    print(f"Best XGBoost Model Accuracy: {xgb_score}")

    # Return the best model and scaler
    best_model = best_rf if rf_score > xgb_score else best_xgb
    return best_model, scaler
