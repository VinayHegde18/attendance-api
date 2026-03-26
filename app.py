from flask import Flask, request, jsonify
from flask import render_template
import sqlite3

app = Flask(__name__)

# Temporary in-memory storage (replace with DB later)
data_store = []

@app.route("/")
def home():
    return "API is running"

@app.route("/attendance", methods=["POST"])
def attendance():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO attendance (empId, eventType, timestamp) VALUES (?, ?, ?)",
        (data.get("empId"), data.get("eventType"), data.get("timestamp"))
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200
    
@app.route("/get_attendance", methods=["GET"])
def get_attendance():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT empId, eventType, timestamp FROM attendance")
    rows = cursor.fetchall()

    conn.close()

    data = [
        {"empId": r[0], "eventType": r[1], "timestamp": r[2]}
        for r in rows
    ]

    return jsonify(data), 200

def get_db():
    return sqlite3.connect("attendance.db")
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empId TEXT,
        eventType TEXT,
        timestamp INTEGER
    )
    """)

    conn.commit()
    conn.close()

# 🔥 CALL THIS ON START
init_db()
@app.route("/admin")
def admin():
    return render_template("admin.html")
    
# IMPORTANT: Render uses this
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
