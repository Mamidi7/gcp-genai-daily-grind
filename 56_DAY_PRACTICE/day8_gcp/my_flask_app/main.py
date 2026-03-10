
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Cloud Run!",
        "status": "deployed",
        "platform": "Google Cloud Run"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/info')
def info():
    return jsonify({
        "app": "Flask on Cloud Run",
        "port": os.environ.get("PORT", 8080)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
