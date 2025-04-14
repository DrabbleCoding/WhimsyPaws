import streamlit as st
import plotly.graph_objects as go
from data_loader import load_emotions_data, load_summary_data, get_emotion_data_for_plotting
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Child Emotion Tracker",
    page_icon="📊",
    layout="wide"
)

# Load data
emotions_data = load_emotions_data()
summary_data = load_summary_data()
dates, emotion_values = get_emotion_data_for_plotting(emotions_data)

# Create the plot
fig = go.Figure()

# Define colors for all emotions in the data
colors = {
    'joy': '#FFD700',      # Gold
    'sadness': '#4169E1',  # Royal Blue
    'fear': '#800080',     # Purple
    'anger': '#FF4500',    # Orange Red
    'embarrassment': '#FF69B4',  # Hot Pink
    'disgust': '#228B22',  # Forest Green
    'neutral': '#808080',  # Gray
    'surprise': '#FFA500'  # Orange
}

# Add lines for each emotion
for emotion in emotion_values.keys():
    fig.add_trace(go.Scatter(
        x=dates,
        y=emotion_values[emotion],
        name=emotion.capitalize(),
        line=dict(color=colors[emotion], width=2),
        mode='lines+markers'
    ))

# Add annotations for important events
for date, description in summary_data:
    if date in dates:
        # Find the maximum emotion value for that date to position the annotation
        max_value = max(emotion_values[emotion][dates.index(date)] for emotion in emotion_values.keys())
        fig.add_annotation(
            x=date,
            y=max_value,
            text=description,
            showarrow=True,
            arrowhead=1,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='black',
            ax=0,
            ay=-40
        )

# Update layout
fig.update_layout(
    title='Child Emotion Tracker',
    xaxis_title='Date',
    yaxis_title='Emotion Intensity',
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ),
    height=600
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Add a section for daily summaries
st.markdown("## Daily Summaries")

# Create a container for the summaries
summary_container = st.container()

# Display summaries in a more readable format
with summary_container:
    for date, description in summary_data:
        # Format the date for display
        display_date = datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')
        
        # Create a card-like display for each summary
        with st.expander(f"{display_date}", expanded=False):
            st.markdown(f"**Event:** {description}")
            
            # Show the emotion values for this day
            if date in dates:
                date_index = dates.index(date)
                st.markdown("**Emotional Response:**")
                
                # Get emotions for this day
                day_emotions = {emotion: emotion_values[emotion][date_index] for emotion in emotion_values.keys()}
                
                # Sort emotions by intensity (highest first)
                sorted_emotions = sorted(day_emotions.items(), key=lambda x: x[1], reverse=True)
                
                # Display top emotions
                for emotion, value in sorted_emotions[:3]:  # Show top 3 emotions
                    if value > 0:  # Only show emotions with positive values
                        st.markdown(f"- **{emotion.capitalize()}**: {value}/10")
                
                # Add a visual indicator of emotional state
                if day_emotions['joy'] > day_emotions['sadness'] and day_emotions['joy'] > day_emotions['fear']:
                    st.markdown("Overall positive emotional state")
                elif day_emotions['sadness'] > day_emotions['joy'] and day_emotions['sadness'] > day_emotions['fear']:
                    st.markdown("Overall negative emotional state")
                elif day_emotions['fear'] > day_emotions['joy'] and day_emotions['fear'] > day_emotions['sadness']:
                    st.markdown("Overall anxious emotional state")
                else:
                    st.markdown("Mixed emotional state")

# Add some context about the visualization
st.markdown("""
### About the Visualization
This chart shows the daily emotional trends of a child over time. Each line represents a different emotion, 
and the markers indicate important events or experiences that occurred on specific days.

- **Joy**: Gold line
- **Sadness**: Blue line
- **Fear**: Purple line
- **Anger**: Orange line
- **Embarrassment**: Pink line
- **Disgust**: Green line
- **Neutral**: Gray line
- **Surprise**: Orange line
""") 