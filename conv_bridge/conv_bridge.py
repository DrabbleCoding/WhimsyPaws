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
import os
from datetime import datetime
import time
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Queue to store messages to be sent to the frontend
message_queue = queue.Queue()

# Debug mode flag
DEBUG_MODE = False

# Track the last known Bot message
last_known_bot_message = None
monitoring_active = False

def get_conversation_path():
    """
    Get the absolute path to the conversation.txt file.
    
    Returns:
        str: Absolute path to the conversation file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', 'data', 'coversation.txt')

def get_last_bot_message():
    """
    Read the conversation.txt file and return the last message from Bot.
    
    Returns:
        str: The last Bot message (without emotional state), or None if no message is found
    """
    try:
        conversation_path = get_conversation_path()
        
        with open(conversation_path, 'r') as file:
            lines = file.readlines()
            
        # Find the last Bot message
        for line in reversed(lines):
            if line.startswith('Bot'):
                # Extract just the message content, removing the emotional state
                message = line.split('):', 1)[1].strip()
                #print(message)
                return message
                
        return None
    except Exception as e:
        print(f"Error reading conversation file: {e}", file=sys.stderr)
        return None

def monitor_for_new_bot_message():
    """
    Monitor the conversation file for new Bot messages.
    """
    global last_known_bot_message, monitoring_active
    
    while monitoring_active:
        try:
            current_last_bot = get_last_bot_message()
            print(current_last_bot)
            
            # If we found a new Bot message
            if current_last_bot != '': # and current_last_bot != last_known_bot_message:
                last_known_bot_message = current_last_bot
                console_input_handler(current_last_bot)
                #monitoring_active = False  # Stop monitoring after finding a new message
                #break
                
            time.sleep(0.25)  # Check every second
        except Exception as e:
            print(f"Error monitoring conversation file: {e}", file=sys.stderr)
            time.sleep(1)

def append_to_conversation(message: str, sender: str = "User"):
    """
    Append a message to the conversation.txt file.
    
    Args:
        message (str): The message to append
        sender (str): The sender of the message (default: "User")
    """
    try:
        conversation_path = get_conversation_path()
        
        # Simply append the message to the file
        with open(conversation_path, 'a') as file:
            file.write(f"{sender}: {message}\n")
            
    except Exception as e:
        print(f"Error appending to conversation file: {e}", file=sys.stderr)

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
    global monitoring_active, last_known_bot_message
    
    data = request.json
    if data and 'message' in data:
        message = data['message']
        print(f"Received chat message: {message}", file=sys.stdout)
        
        # Append the message to the conversation file
        append_to_conversation(message)
        
        # Start monitoring for a new Bot message
        last_known_bot_message = get_last_bot_message()
        monitoring_active = True
        monitor_thread = threading.Thread(target=monitor_for_new_bot_message)
        monitor_thread.daemon = True
        monitor_thread.start()
            
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
        message = message_queue.get() #.get_nowait()
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
    
    # Get and display the last Bot message
    last_known_bot_message = get_last_bot_message()
    if last_known_bot_message:
        print(f"Last Bot message: {last_known_bot_message}", file=sys.stdout)
        console_input_handler(last_known_bot_message)
    else:
        print("No previous Bot message found", file=sys.stderr)
    
    print("Server running on http://localhost:5000", file=sys.stdout)
    app.run(port=5000, debug=True) 