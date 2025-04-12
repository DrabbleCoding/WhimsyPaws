"""
Parent Input UI Module for Child Mental Health Monitoring System

This module provides a modern, user-friendly interface for parents to record
daily observations about their child's well-being.

Author: [Your Name]
Date: [Current Date]
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
from parent_input_module import ParentInputHandler
import threading

class ParentInputUI:
    def __init__(self, root):
        """
        Initialize the Parent Input UI.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("Child Well-being Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize the handler
        self.handler = ParentInputHandler()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50")
        self.style.configure("TLabel", padding=6, background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(
            self.header_frame,
            text="Daily Child Well-being Tracker",
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Create date display
        self.date_frame = ttk.Frame(self.main_frame)
        self.date_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.date_label = ttk.Label(
            self.date_frame,
            text=f"Today's Date: {datetime.now().strftime('%d/%m/%Y')}",
            font=("Helvetica", 12)
        )
        self.date_label.pack(side=tk.LEFT)
        
        # Create input area
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.input_label = ttk.Label(
            self.input_frame,
            text="Enter your observations:",
            font=("Helvetica", 12)
        )
        self.input_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(
            self.input_frame,
            wrap=tk.WORD,
            width=60,
            height=10,
            font=("Helvetica", 11),
            padx=10,
            pady=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Create button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.save_button = ttk.Button(
            self.button_frame,
            text="Save Observation",
            command=self.save_observation,
            style="TButton"
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.view_button = ttk.Button(
            self.button_frame,
            text="View Recent Entries",
            command=self.view_recent_entries
        )
        self.view_button.pack(side=tk.LEFT)
        
        # Set focus to input text
        self.input_text.focus()
    
    def save_observation(self):
        """Save the current observation to the file."""
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Empty Input", "Please enter an observation before saving")
            return
        
        def save_thread():
            self.save_button.config(state="disabled")
            
            success = self.handler.add_observation(message)
            
            if success:
                self.input_text.delete("1.0", tk.END)
                messagebox.showinfo("Success", "Observation saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save observation")
            
            self.save_button.config(state="normal")
        
        # Run save operation in a separate thread
        threading.Thread(target=save_thread).start()
    
    def view_recent_entries(self):
        """Display the most recent entries in a new window."""
        recent_window = tk.Toplevel(self.root)
        recent_window.title("Recent Observations")
        recent_window.geometry("600x400")
        
        # Create text widget for displaying entries
        entries_text = scrolledtext.ScrolledText(
            recent_window,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=("Helvetica", 11),
            padx=10,
            pady=10
        )
        entries_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get and display recent entries
        entries = self.handler.get_latest_observations(10)
        for date, message in entries:
            entries_text.insert(tk.END, f"Date: {date}\n")
            entries_text.insert(tk.END, f"Message: {message}\n\n")
        
        entries_text.config(state="disabled")

def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = ParentInputUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 