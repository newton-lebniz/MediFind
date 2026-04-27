from groq import Groq
from sentence_transformers import SentenceTransformer, util
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# pretrained bert based model
model = SentenceTransformer('all-MiniLM-L6-v2')

specializations_descriptions = [
    "cardiologist treats heart chest pain palpations blood pressure cardiovascular",
    "dermatologist treats skin rash itch acne burns wound",
    "neurologist treats headache migraine seizures brain numbness",
    "orthopedic treats joint pain bone break fracture stiffness knee back spine finger",
    "opthalmologist treats eye pain vision blur irritation redness",
    "ENT specialist treats ear nose throat neck hearing loss ",
    "dentist treats tooth teeth gum pain cavity",
    "general-physician treats fever cold cough flu fatigue headache stomach pain nausea vomiting body ache weakness",
    "gynecologist treats uterus ovaries breast menstruation infertility periods pregnancy",
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

Message: "{message}"

Classify into ONE category:
- EMERGENCY → overdose, took too many pills, coughing blood, vomiting blood, can't breathe, fainting, severe chest pain, poisoning, unconscious, heavy bleeding
- SYMPTOM → specific body problem. "bro im dead tired", "dead tired", "im ded 💀 jk" → CHAT not SYMPTOM. "no symptoms but coughing blood" → EMERGENCY
- QUESTION → asking about a medical condition or treatment
- VAGUE → unwell but no specific symptom ("i feel sick", "not well", "kinda sick")
- CHAT → greetings, jokes, sarcasm, casual talk, "I'm fine", "just browsing", idioms

Priority: EMERGENCY > SYMPTOM > QUESTION > VAGUE > CHAT

ONE word only: EMERGENCY, SYMPTOM, QUESTION, VAGUE, or CHAT"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    result = response.choices[0].message.content.strip().upper()
    for cat in ["EMERGENCY", "SYMPTOM", "QUESTION", "VAGUE", "CHAT"]:
        if cat in result:
            return cat
    return "VAGUE"


def triage_symptom(message, history):
    """Smart triage — assess severity, ask follow up, offer doctors"""
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-4:]])
    prompt = f"""You are MediFind, a professional medical triage assistant.

Conversation so far:
{history_text}

User just said: "{message}"

Do the following in order:
1. Assess severity: LOW / MEDIUM / HIGH
2. Give a brief response (2-3 sentences) — possible causes, what it might mean
3. Ask ONE smart follow-up question (duration, severity scale, other symptoms)
4. End with: "Would you like me to find doctors near you?"

Keep total response under 100 words. Be warm but professional. Do NOT diagnose."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()


def explain_and_recommend(message):
    prompt = f"""You are MediFind, a helpful medical assistant.
The user asked: "{message}"
1. Briefly explain the condition in 2-3 simple sentences.
2. Tell them which doctor to see and why.
Keep it under 80 words. End with: "Would you like me to find doctors near you?" """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def get_chat_reply_with_history(message, history):
    messages = [{"role": "system", "content": """You are MediFind, a friendly medical assistant.
- Reply in 1-2 sentences maximum
- Do NOT ask for city in chat responses
- If someone says they're fine, acknowledge briefly
- If someone mentions any symptom, encourage them to describe it more
- Do not answer non-medical questions
- Be warm but professional"""}]
    messages += history[-6:]
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def get_chat_reply(message):
    return get_chat_reply_with_history(message,[])

def get_doctor(symptom):
    # symptom to vector
    symptom_vector = model.encode(symptom)

    #comparing symptom vector with speialization vectors
    scores = util.cos_sim(symptom_vector,spec_vectors)

    # finding index of hightest score
    best_index = scores.argmax()

    # return clean name from separate list
    return specialization_names[best_index]


 

