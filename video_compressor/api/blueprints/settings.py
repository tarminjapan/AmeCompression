from flask import Blueprint, jsonify
import time

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    })
