import pymysql

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",              
    "database": "caobalhota",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.Cursor,  
    "autocommit": False,        
}

def get_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        return None



get_connection()