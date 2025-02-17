import sqlite3
from sqlite3 import Error

SENSOR_DATA_DB_NAME = "sensor_data.db"

def create_tables():
    """
    Create tables in the SQLite database to store smartwatch data.
    """
    try:
        conn = sqlite3.connect(SENSOR_DATA_DB_NAME)
        cursor = conn.cursor()

        # Create table to store smartwatch data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                heart_rate INTEGER,
                spo2 INTEGER,
                step_count INTEGER,
                battery_level INTEGER,
                device_id TEXT
            )
        ''')
        
        conn.commit()
        print("Database and table created successfully.")
    except Error as e:
        print(f"Error creating database or table: {e}")
    finally:
        if conn:
            conn.close()

# Run this when starting the backend
if __name__ == "__main__":
    create_tables()
