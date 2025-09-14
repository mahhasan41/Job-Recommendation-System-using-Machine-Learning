# config.py

import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",             # Or your MySQL username
        password="",             # Leave empty if no password
        database="resume_system" # Replace with your DB name
    )
