import sqlite3
import datetime
import pickle
import numpy as np
from typing import List, Tuple

DB_NAME = "attendance.db"

def init_db():
    """Initializes the SQLite database with required tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encodings BLOB NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized/checked.")

def save_student(name: str, encodings: List[np.ndarray]):
    """Saves a new student and their face encodings to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    encodings_blob = pickle.dumps(encodings)
    cursor.execute("INSERT INTO students (name, encodings) VALUES (?, ?)", (name, encodings_blob))
    conn.commit()
    conn.close()
    print(f"Student '{name}' registered successfully.")

def get_known_faces() -> Tuple[List[str], List[np.ndarray]]:
    """Retrieves all registered students and their encodings."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, encodings FROM students")
    rows = cursor.fetchall()
    conn.close()

    known_names = []
    known_encodings = []

    for name, encodings_blob in rows:
        encodings = pickle.loads(encodings_blob)
        for enc in encodings:
            known_names.append(name)
            known_encodings.append(enc)
            
    return known_names, known_encodings

def log_attendance(name: str):
    """Logs attendance with a 60-second cooldown."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp FROM attendance_logs 
        WHERE student_name = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (name,))
    row = cursor.fetchone()
    
    should_log = True
    if row:
        try:
            last_time = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            if (datetime.datetime.now() - last_time).total_seconds() < 60:
                should_log = False
        except ValueError:
            pass 

    if should_log:
        cursor.execute("INSERT INTO attendance_logs (student_name, timestamp) VALUES (?, ?)", 
                       (name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        print(f"LOGGED: {name} at {datetime.datetime.now()}")
    
    conn.close()
