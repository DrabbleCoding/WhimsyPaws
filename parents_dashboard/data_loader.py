import json
from datetime import datetime
from typing import Dict, List, Tuple

def load_emotions_data(file_path: str = "emotions.json") -> Dict[str, Dict[str, float]]:
    """Load emotions data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def load_summary_data(file_path: str = "summary.txt") -> List[Tuple[str, str]]:
    """Load summary data from text file."""
    events = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line and line.endswith(':'):
            # This is a date line
            date_str = line[:-1]  # Remove the colon
            # Convert date to YYYY-MM-DD format
            date = datetime.strptime(date_str.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
            
            # Get the description from the next line
            if i + 1 < len(lines):
                description = lines[i + 1].strip()
                if description:  # Only add if there's a description
                    events.append((date, description))
            
            i += 2  # Skip to the next date
        else:
            i += 1  # Skip empty lines or malformed lines
            
    return events

def get_emotion_data_for_plotting(emotions_data: Dict[str, Dict[str, float]]) -> Tuple[List[str], Dict[str, List[float]]]:
    """Process emotions data for plotting."""
    dates = sorted(emotions_data.keys())
    emotions = list(emotions_data[dates[0]].keys())
    
    emotion_values = {emotion: [] for emotion in emotions}
    for date in dates:
        for emotion in emotions:
            emotion_values[emotion].append(emotions_data[date][emotion])
    
    return dates, emotion_values 