"""
Parent Input API Server for Child Mental Health Monitoring System

This module provides a REST API server for the React frontend to interact with
the parent input system.

Author: [Your Name]
Date: [Current Date]
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# File to store observations
OBSERVATIONS_FILE = "observations.json"

def load_observations() -> List[Dict[str, Any]]:
    """Load observations from the JSON file."""
    if os.path.exists(OBSERVATIONS_FILE):
        with open(OBSERVATIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_observations(observations: List[Dict[str, Any]]) -> None:
    """Save observations to the JSON file."""
    with open(OBSERVATIONS_FILE, 'w') as f:
        json.dump(observations, f, indent=2)

@app.route('/api/observations', methods=['GET'])
def get_observations():
    """Get all observations."""
    observations = load_observations()
    return jsonify(observations)

@app.route('/api/observations', methods=['POST'])
def add_observation():
    """Add a new observation."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    observations = load_observations()
    
    new_observation = {
        'id': str(len(observations) + 1),
        'date': datetime.now().isoformat(),
        'message': data['message']
    }
    
    observations.append(new_observation)
    save_observations(observations)
    
    return jsonify(new_observation), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000) 