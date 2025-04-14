# Conversation Bridge

A simple Flask server that acts as a bridge between the emotion-tracker frontend and backend processing.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python conv_bridge.py
```

2. The server will run on http://localhost:5000

3. The server accepts POST requests at `/api/chat` with the following JSON payload:
```json
{
    "message": "user's message text"
}
```

## API Endpoints

### POST /api/chat
- Accepts chat messages from the frontend
- Prints received messages to stdout
- Returns JSON response with status

## Dependencies
- Flask 2.0.1
- Flask-CORS 3.0.10 