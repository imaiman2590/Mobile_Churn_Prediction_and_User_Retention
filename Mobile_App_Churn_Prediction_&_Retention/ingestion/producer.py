from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

actions = ['app_opened', 'feature_used', 'level_completed']

def generate_activity():
    return {
        "user_id": random.randint(1, 1000),
        "action": random.choice(actions),
        "timestamp": datetime.now().isoformat()
    }

while True:
    activity = generate_activity()
    producer.send('user-activity', value=activity)
    print(f"Produced: {activity}")
    time.sleep(1)
