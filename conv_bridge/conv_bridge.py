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
import queue

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Queue to store messages to be sent to the frontend
message_queue = queue.Queue()

def console_input_handler(message: str):
    """
    Handle incoming messages and add them to the queue for the frontend.
    
    Args:
        message (str): The message to send to the frontend
    """
    message_queue.put(message)

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
        # Echo the message back to the frontend
        console_input_handler(message)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "No message provided"}), 400

@app.route('/api/poll', methods=['GET'])
def poll_messages():
    """
    Poll for new messages to display in the frontend.
    
    Returns:
        JSON response with the next message or empty if none available
    """
    try:
        message = message_queue.get_nowait()
        return jsonify({
            "status": "success",
            "message": message
        })
    except queue.Empty:
        return jsonify({
            "status": "success",
            "message": None
        })

if __name__ == '__main__':
    print("Starting conversation bridge server...", file=sys.stdout)
    print("Server running on http://localhost:5000", file=sys.stdout)
    app.run(port=5000, debug=True) 