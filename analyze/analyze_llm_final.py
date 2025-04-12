# pip install google-genai
# pip install langchain

from google import genai
import os, re, json
from langchain.prompts import PromptTemplate
from langchain.chains.base import Chain
from transformers import pipeline

# ----------------------------------
# 🔑 Set up Gemini API client
# ----------------------------------
client = genai.Client(api_key="AIzaSyDaDFAWP27dDnFDY1aio2TC5F3SXL7biig")  

# ----------------------------------
# 🧠 Prompt Template
# ----------------------------------
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

# ----------------------------------
# 📄 Function: Read input file
# ----------------------------------
def read_input_file(path="data/fullcontext.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ File not found:", path)
        return ""

# ----------------------------------
# ✨ Summarize using Gemini
# ----------------------------------
def gemini_summarize(text):
    prompt = summarization_prompt.format(text=text)
    response = client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25",
        contents=prompt
    )
    return response.text

# ----------------------------------
# 💬 Sentiment Analysis
# ----------------------------------
def analyze_sentiment(text, max_length=512):
    daily_summaries = {
        date.strip(): summary.strip()
        for date, summary in re.findall(r"(\d{2}/\d{2}/\d{4}):\n(.+?)(?=\n\d{2}/\d{2}/\d{4}:|\Z)", text, re.DOTALL)
    }

    classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True,
        truncation=True
    )

    def score_to_bucket(score): return max(1, int(round(score * 10)))

    sentiment_by_date = {}
    for date, summary in daily_summaries.items():
        scores = classifier(summary)[0]
        sentiment_by_date[date] = {
            s['label']: score_to_bucket(s['score']) for s in scores
        }

    os.makedirs("output", exist_ok=True)
    with open("output/emotions.json", "w", encoding="utf-8") as f:
        json.dump(sentiment_by_date, f, indent=2, ensure_ascii=False)

    print("✅ Sentiment scores saved to output/emotions.json")
    print("sentiment_by_date", sentiment_by_date)
    return sentiment_by_date

# ----------------------------------
# 🔗 LangChain Custom Chain
# ----------------------------------
class GeminiSentimentChain(Chain):
    @property
    def input_keys(self):
        return ["text"]

    @property
    def output_keys(self):
        return ["summary"]

    def _call(self, inputs):
        text = inputs["text"]
        summary = gemini_summarize(text)
        analyze_sentiment(summary)
        return {"summary": summary}

# ----------------------------------
# 🧠 Main Entry Point
# ----------------------------------
def main():
    input_text = read_input_file("data/fullcontext.txt")
    if not input_text:
        return

    chain = GeminiSentimentChain()
    result = chain.invoke({"text": input_text})
    summary = result["summary"]

    print("\n📋 Summary:\n", summary)

    os.makedirs("output", exist_ok=True)
    with open("output/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("✅ Summary saved to output/summary.txt")

# Run when this file is executed
if __name__ == "__main__":
    main()