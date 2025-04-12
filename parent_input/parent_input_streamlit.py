import streamlit as st
from datetime import datetime
from parent_input_module import ParentInputHandler
import threading

# Set page config
st.set_page_config(
    page_title="Child Well-being Tracker",
    page_icon="📝",
    layout="wide"
)

# Initialize the handler
handler = ParentInputHandler()

# Custom CSS for styling
st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 16px;
        line-height: 1.5;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stExpander {
        background-color: #f0f0f0;
        border-radius: 4px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("Daily Child Well-being Tracker")
st.markdown(f"**Today's Date:** {datetime.now().strftime('%B %d, %Y')}")

# Create two columns for layout
col1, col2 = st.columns([2, 1])

# Input section in the first column
with col1:
    st.markdown("### Enter Your Observations")
    observation = st.text_area(
        "Share your observations about your child's well-being today:",
        height=200,
        placeholder="Enter your observations here..."
    )
    
    if st.button("Save Observation", key="save_button"):
        if observation.strip():
            # Save the observation
            success = handler.add_observation(observation)
            if success:
                st.success("Observation saved successfully!")
                # Clear the text area
                st.experimental_rerun()
            else:
                st.error("Failed to save observation. Please try again.")
        else:
            st.warning("Please enter an observation before saving.")

# Recent entries section in the second column
with col2:
    st.markdown("### Recent Entries")
    
    # Get recent entries
    entries = handler.get_latest_observations(5)
    
    if entries:
        for date, message in entries:
            with st.expander(f"Entry from {date}", expanded=False):
                st.markdown(f"**Date:** {date}")
                st.markdown(f"**Observation:**")
                st.markdown(message)
    else:
        st.info("No entries yet. Start by adding your first observation!")

# Add some helpful information
st.markdown("""
### Tips for Effective Observations
- Be specific about behaviors and emotions you observe
- Note any changes from previous days
- Include both positive and challenging moments
- Consider physical, emotional, and social aspects
""") 