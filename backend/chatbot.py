import openai

openai.api_key = "AIzaSyCAzuheOb2CnUj34gMK3nag9rR7VihcQg0"

def ask_chatbot(query):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content
