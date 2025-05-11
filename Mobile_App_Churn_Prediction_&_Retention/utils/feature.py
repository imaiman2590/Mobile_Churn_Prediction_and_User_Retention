import pandas as pd
from datetime import datetime

def generate_features(user_data):
    """
    Transforms raw user activity data into features for churn prediction.
    
    Args:
        user_data (pd.DataFrame): DataFrame containing raw user activity data.
        
    Returns:
        pd.DataFrame: A DataFrame with engineered features ready for model training or prediction.
    """
    # Feature engineering
    user_data['timestamp'] = pd.to_datetime(user_data['timestamp'])
    
    # Group by user to generate features
    user_stats = user_data.groupby('user_id').agg(
        total_activity_days=('timestamp', lambda x: x.dt.date.nunique()),
        last_seen=('timestamp', 'max'),
        session_count=('action', 'count')
    ).reset_index()

    user_stats['days_since_last'] = (datetime.now() - user_stats['last_seen']).dt.days
    user_stats['avg_session_length'] = user_stats['session_count'] // user_stats['total_activity_days']
    
    # Optional: Add more features or tweak as needed
    return user_stats

def prepare_features_for_model(user_data):
    """
    Prepares the features for input into a machine learning model.
    
    Args:
        user_data (pd.DataFrame): The DataFrame containing user activity data.
        
    Returns:
        X (pd.DataFrame): The feature set.
        y (pd.Series): The target labels (churn or not churn).
    """
    # Generate features from user activity
    user_stats = generate_features(user_data)
    
    # Create target variable - assuming 'days_since_last' > 7 implies churn
    user_stats['churned'] = user_stats['days_since_last'] > 7

    # Select relevant features for the model
    X = user_stats[['total_activity_days', 'session_count', 'days_since_last', 'avg_session_length']]
    y = user_stats['churned'].astype(int)

    return X, y
