import os
from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

# [Optional: Hardcoded password/data for demo]
YOURL_PASSWORD = "your-secret-password"
USER_CONNECTIONS = [
    {"name": "Alice", "type": "family", "last_seen": "2025-07-21"},
    {"name": "Bob", "type": "coworker", "last_seen": "2025-07-19"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            user_input = request.form.get("user_input", "")
            if user_input == YOURL_PASSWORD:
                return jsonify(USER_CONNECTIONS)
            return render_template("thanks.html", input=user_input)
        return render_template("index.html")
    except Exception as e:
        logging.exception("Error serving index page")
        return f"<h1>yourl.cloud</h1><p>Error: {e}</p>", 500

if __name__ == "__main__":
    port = int(os.environ.get
