import mysql.connector
from config.config import DATABASE_CONFIG

def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**DATABASE_CONFIG)