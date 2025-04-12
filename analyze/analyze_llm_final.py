!pip install google-genai

!pip install langchain

from google import genai
import json

client = genai.Client(api_key="AIzaSyDaDFAWP27dDnFDY1aio2TC5F3SXL7biig")

# Import necessary libraries
from langchain.prompts import PromptTemplate
from langchain.chains.base import Chain
from transformers import pipeline
import re, json

# -----------------------------
# Step 1: Define Prompt Templates
# -----------------------------

# Prompt for Gemini summarization
summarization_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You will be given two types of input for multiple days:
1. A conversation between a child (User) and a chatbot (Bot).
2. A daily log message from the child's parents.

Each input is associated with a date in the format DD/MM/YYYY. Your task is to generate a structured summary of the child’s experiences and emotional state for each date.

Please follow these instructions:
- Match the dates from both the conversation and the parent input sections.
- For each date, write **one emotionally focused and insightful sentence**.
- Summarize what happened on that date using both inputs (if available).
- Use **exactly the same date format** as shown in the input (e.g., 01/04/2025).
- Do **not** include weekday names like “Monday” — only the date.
- Focus on the child’s emotions, tone, and overall well-being.
- Avoid narrating or repeating what the Bot said.
- Keep the summary concise, expressive, and relevant.

### Output Format (strictly follow this):
01/04/2025:
<One emotionally-focused summary sentence>

02/04/2025:
<Another emotionally-focused summary sentence>

...

Now process the following input and return only the summary in the format above.

Input:
{text}
"""
)




# Summarization function using Gemini
def gemini_summarize(text):
    # Format the prompt for summarization
    prompt = summarization_prompt.format(text=text)
    # Call the Gemini API using the formatted prompt
    response = client.models.generate_content(
         model="gemini-2.5-pro-exp-03-25",
         contents=prompt
    )
    return response.text




# Function to analyze sentiment, handles long input safely
def analyze_sentiment(text, max_length=512):

    # Parse the input into a dictionary
    daily_summaries = {}
    entries = re.findall(r"(\d{2}/\d{2}/\d{4}):\n(.+?)(?=\n\d{2}/\d{2}/\d{4}:|\Z)", text, re.DOTALL)
    for date, summary in entries:
        daily_summaries[date.strip()] = summary.strip()
    # Initialize the classifier once
    classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True,
        truncation=True
    )
    
    
    
    # Function to scale score (e.g., into 1–10 buckets)
    def score_to_bucket(score, max_score=1.0, buckets=10):
        return max(1, int(round(score * buckets)))  # Ensure at least 1
    
    # Apply sentiment analysis per day
    sentiment_by_date = {}
    
    for date, summary in daily_summaries.items():
        results = classifier(summary)[0]  # Classifier returns a list of lists
        day_scores = {}
        for item in results:
            label = item["label"]
            score = item["score"]
            # Scale to 1–10 buckets
            day_scores[label] = score_to_bucket(score)
        sentiment_by_date[date] = day_scores
    print("sentiment_by_date", sentiment_by_date)
    
    # Save to JSON
    with open("daily_sentiment.json", "w") as f:
        json.dump(sentiment_by_date, f, indent=2)
    
    print("✅ Sentiment scores saved to daily_sentiment.json")





# -----------------------------
# Step 3: Create a Custom LangChain
# -----------------------------

class GeminiSentimentChain(Chain):
    """A LangChain chain that first summarizes text using Gemini and then analyzes its sentiment."""
    
    @property
    def input_keys(self):
        return ["text"]

    @property
    def output_keys(self):
        return ["summary"]

    def _call(self, inputs):
        text = inputs["text"]
        # Step 1: Summarization with Gemini (using the summarization prompt)
        summary = gemini_summarize(text)
        # Step 2: Sentiment analysis on the summary (using the sentiment prompt)
        sentiment = analyze_sentiment(summary)
        return {"summary": summary}





try:
    with open("data/fullcontext.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
except FileNotFoundError:
    print("⚠️ input_text.txt not found. Using default input_text.")


# Your input text


# Instantiate and run the custom chain
chain = GeminiSentimentChain()
result = chain.invoke({"text": input_text})

# Output the results
print("Summary:\n", result["summary"])