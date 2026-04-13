import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def ask_chatbot(query):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content
