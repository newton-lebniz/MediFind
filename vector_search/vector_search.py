from sentence_transformers import SentenceTransformer, util

# pretrained bert based model
model = SentenceTransformer('all-MiniLM-L6-v2')

specializations = [
    "cardiologist treats heart chest pain palpations blood pressure",
    "dermatologist treats skin rash itch itching acne infection",
    "neurologist treats headache migraine seizures brain",
    "orthopedic treats joint pain bone break fracture stiffness",
    "opthalmologist(eye-doctor) treats eye pain vision blur",
    "otolaryngologist treats ear nose throat neck ",
    "dentist treats tooth teeth gum pain",
    "general physician treats fever cold cough flu",
]

# converting specializations to vector 
spec_vectors = model.encode(specializations)

def get_doctor(symptom):
    # symptom to vector
    symptom_vector = model.encode(symptom)

    #comparing symptom vector with speialization vectors
    scores = util.cos_sim(symptom_vector,spec_vectors)

    # finding index of hightest score
    best_index = scores.argmax()

    #extracting doctor name from string
    doctor = specializations[best_index].split(" ")[0]

    return doctor

print(get_doctor("my heart keeps racing"))
print(get_doctor("I have a weird rash on my arm"))
print(get_doctor("my vision is blurry"))
print(get_doctor("I feel dizzy and have chest pressure"))
