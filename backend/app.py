from flask import Flask, request, jsonify
from llm import get_doctor_type
from db import get_doctors_by_specialization

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "symptom" not in data:
        return jsonify({"error": "No symptom provided"}), 400

    symptom = data["symptom"]

    try:
        # 🧠 Step 1: Get doctor type
        doctor_type = get_doctor_type(symptom)

        # 🗄️ Step 2: Get doctors
        doctors = get_doctors_by_specialization(doctor_type)

        if not doctors:
            return jsonify({
                "symptom": symptom,
                "doctor_type": doctor_type,
                "message": "No doctors found"
            })

        return jsonify({
            "symptom": symptom,
            "doctor_type": doctor_type,
            "doctors": doctors
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "MediFind Backend Running 🚀"


if __name__ == "__main__":
    app.run(debug=True)
