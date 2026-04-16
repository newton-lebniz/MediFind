from groq import Groq
from sentence_transformers import SentenceTransformer, util
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("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"))

# pretrained bert based model
model = SentenceTransformer('all-MiniLM-L6-v2')

specializations_descriptions = [
    "cardiologist treats heart chest pain palpations blood pressure",
    "dermatologist treats skin rash itch itching acne infection",
    "neurologist treats headache migraine seizures brain",
    "orthopedic treats joint pain bone break fracture stiffness",
    "opthalmologist(eye-doctor) treats eye pain vision blur",
    "otolaryngologist treats ear nose throat neck ",
    "dentist treats tooth teeth gum pain cavity",
    "general-physician treats fever cold cough flu fatigue",
    "nephrologist treats kidney hypertension dialysis urination",
    "gynecologist uterus ovaries breats menstruation infertility",
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
    "Nephrologist",
    "Gynecologist",
]

# converting specializations to vector 
spec_vectors = model.encode(specializations_descriptions)

def is_symptom(message):
    prompt = f"""You are a medical chatbot classifier.
The user said: "{message}"
Reply with only one word:
- SYMPTOM → if health problem, pain, or medical issue
- CHAT    → if greeting, thanks, or not medical
One word only."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip().upper()
    return "SYMPTOM" in result

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

def get_doctor(symptom):
    # symptom to vector
    symptom_vector = model.encode(symptom)

    #comparing symptom vector with speialization vectors
    scores = util.cos_sim(symptom_vector,spec_vectors)

    # finding index of hightest score
    best_index = scores.argmax()

    # return clean name from separate list
    return specialization_names[best_index]


 

