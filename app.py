from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary in-memory storage (replace with DB later)
data_store = []

@app.route("/")
def home():
    return "API is running"

@app.route("/attendance", methods=["POST"])
def attendance():
    data = request.json

    record = {
        "empId": data.get("empId"),
        "eventType": data.get("eventType"),
        "timestamp": data.get("timestamp")
    }

    data_store.append(record)

    return jsonify({"status": "success"}), 200
    
@app.route("/get_attendance", methods=["GET"])
def get_attendance():
    return jsonify(data_store), 200

# IMPORTANT: Render uses this
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
