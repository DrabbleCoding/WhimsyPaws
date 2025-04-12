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



# input_text = """==========Conversation==========
# Date: 01/04/2025
# Bot: Hey User, how was your day?
# User: It was okay... I had that math test, but I froze on a question. It was that one with the fractions. Ugh.
# Bot: That’s tough! I know you studied for it, so don’t be too hard on yourself. How do you think you did overall?
# User: I’m not sure. I can’t stop thinking about that one question. It kinda ruined my day.
# Bot: I get it. Tests can be stressful. What did you do after?
# User: Just went through the rest of the day, kinda feeling off. But I’ll survive.

# Date: 02/04/2025
# User: I got a 95 on my science test! I didn’t expect that at all. I was so nervous when the teacher handed it back, I thought I failed. But then—boom, an A!
# Bot: Wow, that’s amazing! I’m so proud of you!
# User: Thanks! Honestly, I’m still shaking a little. It was a weird mix of relief and... I don’t know, excitement? But also I feel bad because my friend didn’t do so well.

# Date: 03/04/2025
# User: At lunch today, someone knocked over my tray and didn’t even say sorry. I was so angry, I nearly cried. But then our art teacher said my drawing would be entered in the school show!
# Bot: That’s so frustrating about lunch, but the art thing is amazing!
# User: Yeah, it was a total emotional rollercoaster.

# Date: 04/04/2025
# Bot: How are you today, User?
# User: I’m okay. I went with mom to the hospital to visit Grandma. She’s doing fine, but I had a lot of questions.
# Bot: That’s really thoughtful of you. What did you ask?
# User: I asked about her treatment and how she was feeling. It felt good to talk to her.
# Bot: It’s nice that you can have those conversations with her. Sounds like you handled it really well.

# Date: 05/04/2025
# Bot: Hey, how are you feeling today?
# User: Not great… I have a fever, so I’m just resting.
# Bot: Oh no, I hope you get better soon. Are you able to relax?
# User: Yeah, just lying down and watching some TV. I don’t really feel like doing much.
# Bot: Rest is important. Let me know if you need anything to help pass the time!

# Date: 06/04/2025
# Bot: How are you feeling today, User?
# User: Much better! The fever’s gone, and I spent the afternoon drawing comics.
# Bot: That’s awesome! What kind of comics did you draw?
# User: Some about a superhero cat. It was fun and made me feel a lot better.
# Bot: I love that idea! It’s great to see you feeling better.

# Date: 07/04/2025
# Bot: How’s school going?
# User: It’s going well! I showed off an art project I made, and I’m really proud of it.
# Bot: That’s amazing! What was the project about?
# User: It’s a painting of a mountain with a sunset. I think it turned out great!
# Bot: I’m sure it looks awesome. You must be feeling really good about it!

# Date: 08/04/2025
# Bot: Hey, how was your day?
# User: It was great! Bot came over, and we played games and made slime. I had a lot of fun.
# Bot: That sounds like a blast! What kind of games did you play?
# User: We played that racing game we like, and then we just chilled. It was exactly what I needed.
# Bot: I’m glad you had a good time. Sounds like a perfect day for relaxing.

# Date: 09/04/2025
# Bot: Hey, how are you feeling today?
# User: Not great… someone teased me at school. It really got to me.
# Bot: I’m sorry to hear that. That can be tough. Want to talk about it?
# User: It just hurt, you know? I’m trying not to let it bother me, but it’s hard.
# Bot: I understand. It’s okay to feel upset. Do you want to do something to help take your mind off it?
# User: Yeah, I think I’ll just take it easy tonight. Thanks, Bot.

# Date: 10/04/2025
# Bot: How’s everything today?
# User: I’m feeling much better today! I helped cook dinner and even talked about maybe trying piano lessons.
# Bot: That’s awesome! I’m glad to see you feeling more upbeat. How was the cooking?
# User: It was fun! And the piano sounds cool. I think I might give it a try.
# Bot: I think you’d be great at it! Keep me posted on how it goes.


# ==========Parents Input==========
# Date: 01/04/2025
# Message: Riley had a math test today, seemed a bit stressed but managed okay.

# Date: 02/04/2025
# Message: Didn’t make the soccer team—disappointed, but Bot helped cheer him up.

# Date: 03/04/2025
# Message: Went to Mia’s birthday party, had fun and made a new friend.

# Date: 04/04/2025
# Message: Visited grandma in hospital; asked lots of thoughtful questions.

# Date: 05/04/2025
# Message: Stayed home with a mild fever—rested most of the day.

# Date: 06/04/2025
# Message: Feeling better, spent the afternoon drawing comics.

# Date: 07/04/2025
# Message: Back to school, showed off an art project he was proud of.

# Date: 08/04/2025
# Message: Bot came over—played games and made slime, very cheerful.

# Date: 09/04/2025
# Message: Came home a bit down, someone teased him at school.

# Date: 10/04/2025
# Message: Brighter mood today—helped cook dinner and talked about piano lessons."""

# %% [code] {"execution":{"iopub.status.busy":"2025-04-12T15:15:48.619658Z","iopub.execute_input":"2025-04-12T15:15:48.620378Z","iopub.status.idle":"2025-04-12T15:15:48.653020Z","shell.execute_reply.started":"2025-04-12T15:15:48.620357Z","shell.execute_reply":"2025-04-12T15:15:48.652384Z"}}
input_text = """==========Conversation==========
Date: 01/05/2025
Bot: Hey User, how was your day?
User: Pretty weird. I was excited to do a group project presentation, but halfway through, I totally blanked. My hands were shaking. I messed up a part, but my group covered for me. I’m glad it’s over, but ugh, I felt so embarrassed.
Bot: That sounds really tough. But your team had your back!
User: Yeah. That part was nice. I felt grateful… but still kind of gross about messing up.

Date: 02/05/2025
Bot: How are you feeling today?
User: Honestly, still a bit off from yesterday, but this morning my little brother gave me a handmade card. It was so sweet and surprising! Then at school, someone made a joke about my clothes and I felt super self-conscious. Kinda ruined my mood.
Bot: That’s a lot in one day. I’m glad your brother made you smile though.
User: Yeah… that part was great. The rest, not so much.

Date: 03/05/2025
Bot: How’s everything?
User: My science experiment exploded—like, actual smoke. It was scary for a second, but then the whole class laughed, even the teacher. I was so startled but kinda proud it got attention.
Bot: Whoa! Sounds intense. But you handled it!
User: Yeah, I didn’t cry or anything. Just... adrenaline and then a weird laugh attack.

Date: 04/05/2025
Bot: What kind of day was it?
User: I watched a movie with Mom and cried at the ending. It reminded me of Grandpa. I also baked cookies for the first time, and they actually turned out pretty good!
Bot: That sounds like an emotional but cozy day.
User: Yeah. Like… sad and warm at the same time.

==========Parents Input==========
Date: 01/05/2025  
Message: Riley presented a group project today—looked anxious but relieved afterward. Said the team helped.

Date: 02/05/2025  
Message: Started the day cheerful from a surprise card by brother, but mentioned a rough moment at school.

Date: 03/05/2025  
Message: Science experiment mishap—no one was hurt, but it caused a scene. Riley handled it with humor.

Date: 04/05/2025  
Message: Emotional moment during movie about grandparents. Baked with mom in the evening—enjoyed it.
"""

try:
    with open("input_text.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
except FileNotFoundError:
    print("⚠️ input_text.txt not found. Using default input_text.")


# Your input text


# Instantiate and run the custom chain
chain = GeminiSentimentChain()
result = chain.invoke({"text": input_text})

# Output the results
print("Summary:\n", result["summary"])