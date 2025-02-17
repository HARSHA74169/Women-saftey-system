import sqlite3
import datetime

# Connect to SQLite database
conn = sqlite3.connect("smartwatch_data.db")
cursor = conn.cursor()

# Calculate the timestamp for 7 days ago
seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')  # Format for SQLite

# Delete records older than 7 days
cursor.execute("DELETE FROM your_table WHERE timestamp_column <= ?", (seven_days_ago_str,))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Old records deleted successfully!")
