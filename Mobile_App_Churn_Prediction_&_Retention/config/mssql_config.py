import pyodbc

def get_mssql_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=retention_db;'
        'UID=your_username;'
        'PWD=your_password'
    )
