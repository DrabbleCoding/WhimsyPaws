"""
Parent Input Module for Child Mental Health Monitoring System

This module provides functionality for parents to record daily observations about their child's
well-being. Observations are saved in a structured format with timestamps for later analysis.

Author: [Your Name]
Date: [Current Date]
"""

import datetime
from pathlib import Path
from typing import Optional

class ParentInputHandler:
    """
    A class to handle parent input and storage of child observations.
    
    This class manages the process of recording parent observations about their child's
    daily activities and emotional state, storing them in a structured text file.
    """
    
    def __init__(self, input_file: str = "data/parentsinput.txt"):
        """
        Initialize the ParentInputHandler with the path to the input file.
        
        Args:
            input_file (str): Path to the file where observations will be stored.
                             Defaults to "data/parentsinput.txt"
        """
        self.input_file = Path(input_file)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the input file exists, create it if it doesn't."""
        self.input_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.input_file.exists():
            self.input_file.touch()
    
    def add_observation(self, message: str, date: Optional[datetime.date] = None) -> bool:
        """
        Add a new observation to the input file.
        
        Args:
            message (str): The observation text to be recorded
            date (datetime.date, optional): The date of the observation.
                                          If None, current date is used.
        
        Returns:
            bool: True if the observation was successfully added, False otherwise
        """
        try:
            if date is None:
                date = datetime.date.today()
            
            # Format the date as DD/MM/YYYY
            formatted_date = date.strftime("%d/%m/%Y")
            
            # Prepare the entry
            entry = f"Date: {formatted_date}\nMessage: {message}\n\n"
            
            # Append the entry to the file
            with open(self.input_file, 'a', encoding='utf-8') as f:
                f.write(entry)
            
            return True
        except Exception as e:
            print(f"Error adding observation: {str(e)}")
            return False
    
    def get_latest_observations(self, count: int = 5) -> list:
        """
        Retrieve the most recent observations from the file.
        
        Args:
            count (int): Number of most recent observations to retrieve.
                        Defaults to 5.
        
        Returns:
            list: List of tuples containing (date, message) pairs
        """
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split entries by double newlines
            entries = content.strip().split('\n\n')
            
            # Process entries and extract date and message
            observations = []
            for entry in entries:
                if not entry.strip():
                    continue
                lines = entry.split('\n')
                date = lines[0].replace('Date: ', '')
                message = lines[1].replace('Message: ', '')
                observations.append((date, message))
            
            # Return the most recent observations
            return observations[-count:]
        except Exception as e:
            print(f"Error retrieving observations: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    # Create an instance of the handler
    handler = ParentInputHandler()
    
    # Example: Add a new observation
    success = handler.add_observation("Child had a great day at school and made new friends")
    if success:
        print("Observation added successfully!")
    
    # Example: Get latest observations
    latest = handler.get_latest_observations(3)
    print("\nLatest observations:")
    for date, message in latest:
        print(f"Date: {date}")
        print(f"Message: {message}\n") 