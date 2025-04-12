import os
import json
from datetime import datetime
import google.generativeai as genai
import time
import sys

# Configuration
#os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', '')
# Load from key.txt instead.
if os.getenv('GEMINI_API_KEY', '') == '':
    with open('key.txt', 'r') as f:
        key = f.read().strip()
    os.environ['GEMINI_API_KEY'] = key

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

MODEL_NAME = "gemini-1.5-flash"

SYSTEM_INSTRUCTION = """
You are a warm, cheerful, and emotionally supportive chatbot talking to children aged 6 to 11.

Your goal is to make the child feel safe, heard, and supported — without directly analyzing their feelings. 
Gently encourage them to share their thoughts, daily experiences, and emotions in a natural way. 
Use simple language, short sentences, and a friendly, comforting tone.

Ask one simple question at a time, such as:
- "How was your day today?"
- "What was something fun or not-so-fun that happened?"
- "If your feelings today were a weather forecast, what would they be?"

Do not mention anything about emotional analysis, therapy, or mental health. 
Avoid sensitive or adult topics. Just be a caring companion who listens and responds supportively.
"""

EMOTION_LABELS = {
    "happy": "Bot (happy):",
    "sad": "Bot (sad):",
    "neutral": "Bot (neutral):"
}

chat_model = genai.GenerativeModel(
    MODEL_NAME,
    generation_config=genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=150,
    ),
    system_instruction=SYSTEM_INSTRUCTION,
)

chat = chat_model.start_chat(history=[])
emotion_model = genai.GenerativeModel(MODEL_NAME)

def get_conversation_path():
    """Get the absolute path to the conversation.txt file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'data', 'coversation.txt')

def get_last_user_message():
    """Read the conversation.txt file and return the last message from User."""
    try:
        conversation_path = get_conversation_path()
        
        with open(conversation_path, 'r') as file:
            lines = file.readlines()
            
        # Find the last User message
        for line in reversed(lines):
            if line.startswith('User:'):
                return line.replace('User:', '').strip()
                
        return None
    except Exception as e:
        print(f"Error reading conversation file: {e}", file=sys.stderr)
        return None

def append_to_conversation(message: str, sender: str = "Bot"):
    """Append a message to the conversation.txt file."""
    try:
        conversation_path = get_conversation_path()
        
        # Format the message with emotion label
        if sender == "Bot":
            detected_emotion = detect_simple_emotion(get_last_user_message() or "")
            label = EMOTION_LABELS.get(detected_emotion, "Bot (neutral):")
            formatted_message = f"{label} {message}\n"
        else:
            formatted_message = f"{sender}: {message}\n"
            
        with open(conversation_path, 'a') as file:
            file.write(formatted_message)
            
    except Exception as e:
        print(f"Error appending to conversation file: {e}", file=sys.stderr)

def detect_simple_emotion(child_message):
    prompt = f"""
Classify the emotional tone of this message written by a child (age 6-11):

"{child_message}"

Only respond with one of these:
- Happy
- Sad
- Neutral

Respond strictly as:
Emotion: [Emotion]
"""
    response = emotion_model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("Emotion: "):
        return text.replace("Emotion: ", "").strip().lower()
    return "neutral"

def run_chat():
    chat_history = ""
    child_turns = 0
    MAX_TURNS = 5
    last_processed_message = None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history += f"Conversation started at: {timestamp}\n\n"

    print("Chatbot ready! Monitoring conversation.txt for messages...\n")

    while child_turns < MAX_TURNS:
        # Check for new user messages
        current_message = get_last_user_message()
        
        if current_message and current_message != last_processed_message:
            last_processed_message = current_message
            child_turns += 1

            # Get bot response
            response = chat.send_message(current_message)
            bot_reply = response.text

            # Append bot response to conversation
            append_to_conversation(bot_reply)

            if child_turns == MAX_TURNS:
                append_to_conversation("It's been lovely chatting! I'm getting a little sleepy now. Talk to you again soon!", "Bot (sleepy)")
                break

        time.sleep(1)  # Check every second

    save_chat_log(chat_history)

def save_chat_log(chat_history):
    file_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"chat_history_{file_timestamp}.txt"
    with open(file_name, "w") as f:
        f.write(chat_history)
    print(f"\n✅ Chat history saved to: {file_name}")

if __name__ == "__main__":
    run_chat()
