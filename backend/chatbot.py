import sys
sys.path.append('../vector_search')
from vector_search import get_chat_reply

def ask_chatbot(query):
    return get_chat_reply(query)
