# GitHub Webhook Event Tracker

This project demonstrates an end-to-end GitHub webhook integration using Flask.
It listens to GitHub repository events (Push, Pull Request, and Merge), stores
clean and minimal event data in MongoDB, and displays recent activity in a simple
UI that polls the backend every 15 seconds.

---

## Architecture Overview

GitHub Repository (action-repo)
|
| GitHub Webhook Events
v
Flask Backend (webhook-repo)
|
| Store parsed events
v
MongoDB
|
| Poll every 15 seconds
v
Browser UI


---

## Supported Events

- **Push**
- **Pull Request (opened)**
- **Merge** (Pull Request closed with `merged = true`)

Each event is stored as a single document in MongoDB with only the required fields.

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MongoDB
- **Frontend:** HTML + Vanilla JavaScript
- **Integration:** GitHub Webhooks
- **Local Webhook Testing:** ngrok

---

## MongoDB Event Schema

```json
{
  "event_type": "push | pull_request | merge",
  "author": "username",
  "from_branch": "source-branch",
  "to_branch": "target-branch",
  "timestamp": "ISO-8601 UTC timestamp"
}
```

## Prerequisites

Python 3.9+

MongoDB (local or MongoDB Atlas)

Git

ngrok


## Setup Steps

git clone webhook-repo-url

cd webhook-repo

python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python app.py

The application will start at : http://localhost:5000

---

Setting Up GitHub Webhooks (Local Testing)

Since GitHub cannot access localhost, ngrok is used.

Start ngrok with : ngrok http 5000

Copy the generated HTTPS URL, for example : https://abcd1234.ngrok.io


## Configure Webhook in action-repo

- Go to Settings → Webhooks → Add webhook
- Payload URL: https://abcd1234.ngrok.io/webhook

- Content type: application/json

- Events: Push  and Pull requests

- Save webhook
