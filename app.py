from flask import Flask, jsonify, request
from db import events_collection

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "Flask + MongoDB connected"})

@app.route("/test-insert", methods=["POST"])
def test_insert():
    sample_event = {
        "event_type": "push",
        "author": "TestUser",
        "from_branch": None,
        "to_branch": "main",
        "timestamp": "2026-01-01T10:00:00Z"
    }

    events_collection.insert_one(sample_event)
    return jsonify({"message": "Event inserted"}), 201

@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
