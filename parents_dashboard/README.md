# Child Emotion Tracker

A Streamlit web application that visualizes a child's daily emotional trends using Plotly. The app displays interactive charts showing different emotions over time and annotates important events.

## Features

- Interactive Plotly line chart showing multiple emotions
- Event annotations with descriptions
- Clean, modern interface
- Responsive design

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the App

To run the app, use the following command:
```bash
streamlit run app.py
```

The app will open in your default web browser. If it doesn't, you can access it at http://localhost:8501

## Data Files

The app requires two data files:

1. `emotions.json`: Contains daily emotion scores
2. `summary.txt`: Contains daily event descriptions

Make sure these files are in the root directory of the project.

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── data_loader.py      # Data loading and processing functions
├── emotions.json       # Emotion data
├── summary.txt         # Event descriptions
├── requirements.txt    # Python dependencies
└── README.md          # This file
``` 