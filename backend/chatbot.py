import openai

openai.api_key ="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"

def ask_chatbot(query):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content
