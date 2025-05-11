from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from config.mssql_config import get_mssql_connection

app = FastAPI()

class Feedback(BaseModel):
    user_id: int
    true_churn: bool

@app.post("/feedback")
def submit(feedback: Feedback):
    conn = get_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        MERGE churn_feedback AS target
        USING (SELECT ? AS user_id) AS src
        ON target.user_id = src.user_id
        WHEN MATCHED THEN
            UPDATE SET true_churn = ?, feedback_time = ?
        WHEN NOT MATCHED THEN
            INSERT (user_id, true_churn, feedback_time)
            VALUES (?, ?, ?)
    """, feedback.user_id, feedback.true_churn, datetime.now(), feedback.user_id, feedback.true_churn, datetime.now())
    conn.commit()
    return {"message": "Feedback saved"}
