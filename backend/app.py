from flask import Flask, jsonify

from feature_flags import get_flag

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/feature-flags")
def flags():
    return jsonify({
        "NEW_DASHBOARD_ENABLED": get_flag("NEW_DASHBOARD_ENABLED")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").getenv("PORT", "8000")))
