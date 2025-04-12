"""
Parent Input API Server for Child Mental Health Monitoring System

This module provides a REST API server for the React frontend to interact with
the parent input system using the ParentInputHandler for data management.

Author: [Your Name]
Date: [Current Date]
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from parent_input_module import ParentInputHandler
from typing import List, Dict, Any
import re
import threading
import time
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the handler
handler = ParentInputHandler()

class ContextUpdater:
    def __init__(self):
        self.running = True
        self.parents_file = "data/parentsinput.txt"
        self.conversation_file = "data/coversation.txt"
        self.output_file = "data/fullcontext.txt"
        
    def update_context(self):
        while self.running:
            try:
                # Read parents input
                with open(self.parents_file, 'r', encoding='utf-8') as f:
                    parents_content = f.read()
                
                # Read conversation
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    conversation_content = f.read()
                
                # Combine content
                combined_content = f"==========Conversation==========\n{conversation_content}\n\n==========Parents Input==========\n{parents_content}"
                
                # Write to fullcontext.txt
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    f.write(combined_content)
                
            except Exception as e:
                print(f"Error updating context: {str(e)}")
            
            time.sleep(5)  # Wait 5 seconds before next update
    
    def start(self):
        self.thread = threading.Thread(target=self.update_context)
        self.thread.daemon = True  # Thread will be killed when main program exits
        self.thread.start()
    
    def stop(self):
        self.running = False
        self.thread.join()

# Initialize and start the context updater
context_updater = ContextUpdater()
context_updater.start()

def parse_date(date_str: str) -> str:
    """Parse date string from the file format to ISO format."""
    # Try to parse the date in DD/MM/YYYY format
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.isoformat()
    except ValueError:
        return date_str  # Return original if parsing fails

def observation_to_dict(date: str, message: str) -> Dict[str, Any]:
    """Convert observation tuple to dictionary format."""
    # Clean up the date string by removing 'Date: ' prefix if present
    clean_date = date.replace('Date: ', '')
    return {
        'id': str(hash(clean_date + message)),  # Generate a unique ID
        'date': parse_date(clean_date),
        'message': message.strip()
    }

@app.route('/api/observations', methods=['GET'])
def get_observations():
    """Get all observations."""
    try:
        # Get the latest observations (using a large number to get all)
        observations = handler.get_latest_observations(1000)
        # Convert to the expected format
        formatted_observations = [
            observation_to_dict(date, message)
            for date, message in observations
        ]
        return jsonify(formatted_observations)
    except Exception as e:
        print(f"Error in GET /api/observations: {str(e)}")  # Debug logging
        return jsonify({'error': str(e)}), 500

@app.route('/api/observations', methods=['POST'])
def add_observation():
    """Add a new observation."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        # Add the observation using the handler
        success = handler.add_observation(data['message'])
        
        if not success:
            return jsonify({'error': 'Failed to save observation'}), 500

        # Get the latest observation to return
        latest = handler.get_latest_observations(1)
        if latest:
            date, message = latest[0]
            return jsonify(observation_to_dict(date, message)), 201
        else:
            return jsonify({'error': 'Failed to retrieve saved observation'}), 500

    except Exception as e:
        print(f"Error in POST /api/observations: {str(e)}")  # Debug logging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 