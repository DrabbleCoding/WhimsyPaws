import os
import json
from datetime import datetime
import google.generativeai as genai

# Configuration
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', '')
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

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history += f"Conversation started at: {timestamp}\n\n"

    print("Chatbot ready! (Type 'exit' to quit)\n")

    while child_turns < MAX_TURNS:
        child_input = input("Child: ")
        if child_input.lower() == "exit":
            break

        chat_history += f"Child: {child_input}\n"
        child_turns += 1

        detected_emotion = detect_simple_emotion(child_input)
        response = chat.send_message(child_input)
        bot_reply = response.text

        label = EMOTION_LABELS.get(detected_emotion, "Bot:")
        print(f"{label} {bot_reply}")
        chat_history += f"Chatbot: {bot_reply}\n"

        if child_turns == MAX_TURNS:
            print("Bot (sleepy): It's been lovely chatting! I'm getting a little sleepy now. Talk to you again soon!")
            break

    save_chat_log(chat_history)

def save_chat_log(chat_history):
    file_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"chat_history_{file_timestamp}.txt"
    with open(file_name, "w") as f:
        f.write(chat_history)
    print(f"\n✅ Chat history saved to: {file_name}")

if __name__ == "__main__":
    run_chat()
