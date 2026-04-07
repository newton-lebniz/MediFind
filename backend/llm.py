def get_doctor_type(symptom):
    
    symptom = symptom.lower()

    if "heart" in symptom.lower() or "chest" in symptom.lower() or "racing" in symptom.lower():
        return "Cardiologist"
    elif "skin" in symptom.lower() or "rash" in symptom.lower():
        return "Dermatologist"
    elif "headache" in symptom.lower() or "brain" in symptom.lower():
        return "Neurologist"
    elif "fever" in symptom.lower() or "cold" in symptom.lower():
        return "General Physician"
    elif "bone pain" in symptom.lower() or "limited movement" in symptom.lower() or "stiffness" in symptom.lower() or "joint pain" in symptom.lower() or "swelling" in symptom.lower():
        return "Orthopedic" 
    else:
        return "General Physician"
