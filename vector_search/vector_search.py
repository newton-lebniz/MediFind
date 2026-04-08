from sentence_transformers import SentenceTransformer, util

# pretrained bert based model
model = SentenceTransformer('all-MiniLM-L6-v2')

specializations_descriptions = [
    "cardiologist treats heart chest pain palpations blood pressure",
    "dermatologist treats skin rash itch itching acne infection",
    "neurologist treats headache migraine seizures brain",
    "orthopedic treats joint pain bone break fracture stiffness",
    "opthalmologist(eye-doctor) treats eye pain vision blur",
    "otolaryngologist treats ear nose throat neck ",
    "dentist treats tooth teeth gum pain",
    "general-physician treats fever cold cough flu",
    "nephrologist treats kidney hypertension dial",
    "gynecologist uterus ovaries breats menstruation infertility",
]

# these are the clean names that match your database exactly
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

def get_doctor(symptom):
    # symptom to vector
    symptom_vector = model.encode(symptom)

    #comparing symptom vector with speialization vectors
    scores = util.cos_sim(symptom_vector,spec_vectors)

    # finding index of hightest score
    best_index = scores.argmax()

    # return clean name from separate list
    return specialization_names[best_index]

# test it
if __name__ == "__main__":
    tests = [
        "my heart keeps racing",
        "I have a weird rash on my arm",
        "my vision is blurry",
        "my eye burns",
        "I feel dizzy and have chest pressure",
        "my tooth hurts",
        "I have fever and cough",
        "my knee is stiff",
        "ear pain and hearing loss",
    ]
    for t in tests:
        print(f"{t:45} → {get_doctor(t)}")



 

