from kafka import KafkaConsumer
import json
import pyodbc
from mssql_config import get_mssql_connection

consumer = KafkaConsumer(
    'user-activity',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='retention-group'
)

conn = get_mssql_connection()
cursor = conn.cursor()

cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user_activity')
    CREATE TABLE user_activity (
        user_id INT,
        action NVARCHAR(255),
        timestamp DATETIME
    )
""")
conn.commit()

buffer = []

for msg in consumer:
    data = msg.value
    buffer.append((data['user_id'], data['action'], data['timestamp']))

    if len(buffer) >= 10:
        cursor.executemany("""
            INSERT INTO user_activity (user_id, action, timestamp)
            VALUES (?, ?, ?)
        """, buffer)
        conn.commit()
        print(f"Inserted {len(buffer)} records.")
        buffer.clear()
