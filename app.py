import logging
import os
import time

from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return jsonify({
        "message": "Hello from DevOps!",
        "status": "success",
        "project": "flask-hello-devops",
        "env": os.getenv("FLASK_ENV", "dev")
    })


@app.route('/health')
def health():
    return jsonify({"status": "ok", "uptime": time.time()})


@app.route('/ready')
def ready():
    return jsonify({"status": "ready"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
