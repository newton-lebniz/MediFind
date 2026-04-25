from groq import Groq
from sentence_transformers import SentenceTransformer, util
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# pretrained bert based model
model = SentenceTransformer('all-MiniLM-L6-v2')

specializations_descriptions = [
    "cardiologist treats heart chest pain palpations blood pressure",
    "dermatologist treats skin rash itch itching acne infection burns wound",
    "neurologist treats headache migraine seizures brain",
    "orthopedic treats joint pain bone break fracture stiffness",
    "opthalmologist(eye-doctor) treats eye pain vision blur",
    "otolaryngologist treats ear nose throat neck ",
    "dentist treats tooth teeth gum pain cavity",
    "general-physician treats fever cold cough flu fatigue",
    "gynecologist uterus ovaries breats menstruation infertility",
    "nephrologist treats kidney hypertension dialysis urination",
]

specialization_names = [
    "Cardiologist",
    "Dermatologist",
    "Neurologist",
    "Orthopedic",
    "Ophthalmologist",
    "ENT Specialist",
    "Dentist",
    "General Physician",
    "Gynecologist",
    "Nephrologist",
]

# converting specializations to vector 
spec_vectors = model.encode(specializations_descriptions)

def classify_message(message):
    prompt = f"""You are a medical chatbot classifier.
The user said: "{message}"

Rules:
- VAGUE  → if the message is too general with NO specific body part or symptom mentioned. Examples: "i'm not well", "i feel sick", "not feeling good", "i'm unwell", "something is wrong"
- SYMPTOM → if a SPECIFIC body part or problem is mentioned. Examples: "chest pain", "headache", "skin rash", "my knee hurts"
- QUESTION → if asking to explain a medical condition. Examples: "what is diabetes", "explain folliculitis"
- CHAT → if greeting or non-medical. Examples: "hi", "thanks", "how are you"

Reply with ONE word only: VAGUE, SYMPTOM, QUESTION, or CHAT"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip().upper()

def explain_and_recommend(message):
    prompt = f"""You are MediFind, a helpful medical assistant.
The user said: "{message}"
Do two things:
1. Briefly explain the condition they mentioned in 2-3 simple sentences.
2. Tell them which type of doctor they should see and why.
Keep it friendly, simple, and under 100 words total.
End with: "Would you like me to find doctors near you?" """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def get_chat_reply(message):
    prompt = f"""You are MediFind, a friendly medical assistant chatbot.
The user said: "{message}"
Reply in 1-2 short friendly sentences.
If they seem unwell, gently ask them to describe their symptoms."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def get_chat_reply_with_history(message, history):
    messages = [{"role": "system", "content": "You are MediFind, a friendly medical assistant chatbot. Help users find the right doctor based on symptoms. Keep replies short and helpful. If someone describes a symptom, ask for their city to find nearby doctors."}]
    messages += history
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def get_doctor(symptom):
    # symptom to vector
    symptom_vector = model.encode(symptom)

    #comparing symptom vector with speialization vectors
    scores = util.cos_sim(symptom_vector,spec_vectors)

    # finding index of hightest score
    best_index = scores.argmax()

    # return clean name from separate list
    return specialization_names[best_index]


 

