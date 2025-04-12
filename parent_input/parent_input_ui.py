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

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the handler
handler = ParentInputHandler()

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