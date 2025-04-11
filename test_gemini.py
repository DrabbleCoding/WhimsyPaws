from google import genai

client = genai.Client(api_key="AIzaSyDaDFAWP27dDnFDY1aio2TC5F3SXL7biig")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain diabetes to me like I am a child who is diagnosed with diabetes"
)
print(response.text)