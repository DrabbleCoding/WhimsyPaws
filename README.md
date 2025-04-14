
# 🧸 Child Chatbot with Emotion Detection (Gemini API)

This is a simple, supportive chatbot designed for children aged 6–11. It uses Google’s Gemini model to engage in friendly, emotionally aware conversations, and labels responses based on emotional tone (Happy, Sad, Neutral).

## 💡 Features

- Cheerful chatbot for kids aged 6–11
- Emotion detection based on child input
- Supportive, age-appropriate conversation
- Saves chat history to a `.txt` file

## 🚀 How to Run

### 1. Python Setup

```bash
pip install -r requirements.txt
```

### 2. npm Setup

```bash
cd parents_dashboard/emotion-tracker
npm install
```

### 3. Set your Gemini API Key

```bash
export GEMINI_API_KEY=your-gemini-api-key
```

Alternatively, you can store the key in a file in the root directory called `key.txt`

### 4. Start the chatbot back end

```bash
python child_chatbot.py
```

### 5. Start the back end bridge
In a new terminal, run the following:

```bash
cd conv_bridge
python conv_bridge.py
```

### 6. Start up the GUI
In a new terminal, run the following: 

```bash
cd parents_dashboard/emotion-tracker
npm start
```

### 7. Enjoy!

The default Parent password is `1234` and the default Child password is `5678`