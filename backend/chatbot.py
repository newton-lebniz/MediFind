import openai

openai.api_key ="AIzaSyB-CXbRUKUl4YRe3BqwB0YQ_2QgB838r_c"

def ask_chatbot(query):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content
