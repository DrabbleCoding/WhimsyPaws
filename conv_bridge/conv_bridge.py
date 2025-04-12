"""
Conversation Bridge Server

This server acts as a bridge between the emotion-tracker frontend and any backend processing.
It receives chat messages from the frontend and prints them to stdout.

Usage:
    python conv_bridge.py

The server runs on http://localhost:5000 and accepts POST requests at /api/chat.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/chat', methods=['POST'])
def receive_chat():
    """
    Receive chat messages from the frontend.
    
    Expected JSON payload:
    {
        "message": "user's message text"
    }
    
    Returns:
        JSON response with status and optional message
    """
    data = request.json
    if data and 'message' in data:
        message = data['message']
        print(f"Received chat message: {message}", file=sys.stdout)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "No message provided"}), 400

if __name__ == '__main__':
    print("Starting conversation bridge server...", file=sys.stdout)
    print("Server running on http://localhost:5000", file=sys.stdout)
    app.run(port=5000, debug=True) 