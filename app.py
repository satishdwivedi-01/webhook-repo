from flask import Flask, jsonify, request
from db import events_collection

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "Running"})

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    # 1️⃣ PUSH EVENT
    if event_type == "push":
        author = payload.get("pusher", {}).get("name")
        ref = payload.get("ref")
        to_branch = ref.split("/")[-1] if ref else None
        timestamp = payload.get("head_commit", {}).get("timestamp")

        event_doc = {
            "event_type": "push",
            "author": author,
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        events_collection.insert_one(event_doc)

    # 2️⃣ PULL REQUEST EVENTS
    elif event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})

        author = pr.get("user", {}).get("login")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")

        # PR CREATED
        if action == "opened":
            timestamp = pr.get("created_at")

            event_doc = {
                "event_type": "pull_request",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            events_collection.insert_one(event_doc)

        # PR MERGED (BONUS)
        elif action == "closed" and pr.get("merged") is True:
            timestamp = pr.get("merged_at")

            event_doc = {
                "event_type": "merge",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            events_collection.insert_one(event_doc)

    return jsonify({"message": "Webhook processed"}), 200



@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

