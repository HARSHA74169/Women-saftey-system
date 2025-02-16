import sqlite3

DB_NAME = "sensor_data.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table to store smartwatch data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            heart_rate INTEGER,
            step_count INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

# Run this when starting the backend
if __name__ == "__main__":
    create_tables()
