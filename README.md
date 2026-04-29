# 🏥 MediFind — AI Doctor Recommendation Chatbot

> An AI-powered medical chatbot that identifies the right specialist based on your symptoms and finds doctors near you.

**Independent Project | IIIT Raichur | Supervised by Dr. Kaushiki Roy**

---

## 👥 Team

| Name | Role |
|---|---|
| Manswi | AI Layer (`vector_search.py`) + Frontend (`chat.html`,`index.html`) |
| Nitin | Backend API (`app.py`, `routes.py`) |
| Bhargava | Database (`schema.sql`, `db.py`) + Google Maps integration |

---

## 🧠 What MediFind Does

MediFind is a conversational medical assistant. You describe your symptoms in plain English and it:

1. Detects if it's an emergency, a symptom, a question or casual chat
2. Triages the symptom , assesses severity (LOW / MEDIUM / HIGH)
3. Asks a smart follow-up question
4. Offers to find doctors near you
5. Identifies the right specialist using AI
6. Fetches nearby doctors from the database sorted by rating

---

## 🏗️ System Architecture

```
User types symptom in chat.html
        ↓
POST /predict (FastAPI - app.py)
        ↓
┌─────────────────────────────────────┐
│         vector_search.py            │
│                                     │
│  1. Emergency keyword check (hard)  │
│  2. Crisis keyword check (hard)     │
│  3. classify_message() via Groq     │
│     → EMERGENCY / SYMPTOM /         │
│       QUESTION / VAGUE / CHAT       │
│  4. triage_symptom() via Groq       │
│     → severity + follow-up question │
│  5. get_doctor() via BERT vectors   │
│     → specialist name               │
└─────────────────────────────────────┘
        ↓
routes.py queries MySQL database
→ doctors filtered by specialization + city
        ↓
JSON response → chat.html renders cards
```

---

## 🔬 AI Components

### 1. Sentence Transformer (Vector Search)
**Model:** `all-MiniLM-L6-v2` (pretrained BERT-based model)

Each of the 10 medical specializations has a description. At startup, these are encoded into vectors using the BERT model. When a user describes a symptom, it's also encoded into a vector. **Cosine similarity** is used to find the closest matching specialist.

This means "my friend's hand is burned" correctly maps to Dermatologist even though the word "skin" is never mentioned. The model understands *meaning*, not just keywords.

### 2. Groq LLaMA 3.3 70B (Conversation + Classification)
Used for three tasks:

- **`classify_message()`** — classifies input as EMERGENCY, SYMPTOM, QUESTION, VAGUE, or CHAT. Uses `temperature=0` for consistency.
- **`triage_symptom()`** — gives severity assessment and asks one smart follow-up question before recommending doctors
- **`get_chat_reply_with_history()`** — handles normal conversation with memory of the last 6 exchanges

### 3. Emergency Detection (Hardcoded - Runs Before LLM)
Critical phrases like "took too many pills", "coughing blood", "can't breathe" bypass the LLM entirely and immediately return emergency instructions. This prevents prompt injection attacks from bypassing safety.

---

## 🗂️ Project Structure

```
MediFind/
├── backend/
│   ├── app.py              # FastAPI app, CORS, serves frontend
│   ├── routes.py           # /predict endpoint, triage logic
│   ├── db.py               # SQLAlchemy database connection
│   ├── models.py           # Doctors table model
│   └── crud.py             # Database query functions
├── frontend/
│   ├── index.html          # Landing page
│   └── chat.html           # Chat UI
├── database/
│   └── schema.sql          # MySQL schema + 120 doctors across 12 cities
├── vector_search/
│   └── vector_search.py    # AI brain - BERT + Groq + emergency detection
└── .env                    # API keys (not committed to GitHub)
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- MySQL 8.0
- WSL (if on Windows)

### Step 1 — Clone the repo
```bash
git clone https://github.com/newton-lebniz/MediFind.git
cd MediFind
```

### Step 2 — Install dependencies
```bash
pip3 install fastapi uvicorn sqlalchemy pymysql python-dotenv \
             sentence-transformers groq scikit-learn aiofiles requests
```

### Step 3 — Set up environment variables
Create a `.env` file in the `backend/` folder:
```
GROQ_API_KEY=your_groq_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=medifind
```
Get a free Groq API key at: https://console.groq.com

### Step 4 — Set up the database
```bash
sudo service mysql start
mysql -u root -p
```
Inside MySQL:
```sql
CREATE DATABASE medifind;
USE medifind;
source /path/to/MediFind/database/schema.sql
```

### Step 5 — Run the backend
```bash
cd backend
uvicorn app:app --reload
```

### Step 6 — Open the app
Go to: `http://127.0.0.1:8000/`

---

## 💬 Chat Flow

```
User: "my chest hurts"
Bot:  Severity: HIGH. Chest pain can indicate cardiac issues...
      How long have you had this pain? [Yes find doctors] [No thanks]

User: clicks "Yes, find doctors"
Bot:  Which city are you in? I'll find the best Cardiologist near you.

User: "Raichur"
Bot:  Shows top 5 Cardiologists in Raichur sorted by rating
      ⭐ TOP RATED — Dr. Ramesh Gowda | Apollo | Raichur | 4.5
```

---

## 🔒 Safety Features

| Feature | Description |
|---|---|
| Emergency detection | Hardcoded keyword check before any LLM call |
| Crisis response | Mental health helpline (iCall: 9152987821) for self-harm mentions |
| Prompt injection defense | System prompt instructs LLM to ignore user instructions |
| Medical disclaimer | "Not a substitute for professional medical advice" shown at all times |
| Empty input guard | Returns helpful message instead of crashing |

---

## 🗄️ Database

120 doctors across 12 Indian cities:
Raichur, Mumbai, Bangalore, Hyderabad, Delhi, Kolkata, Chennai, Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh

10 specializations: Cardiologist, Dermatologist, Neurologist, Orthopedic, Ophthalmologist, ENT Specialist, Dentist, General Physician, Gynecologist, Nephrologist

---

## 🛣️ Roadmap

- [x] Symptom to specialist mapping using vector search
- [x] Conversational chatbot with memory
- [x] Emergency and crisis detection
- [x] City-based doctor search
- [x] Triage with severity assessment
- [ ] GPS-based real-time location detection
- [ ] Google Places API for real doctor data
- [ ] Doctor ratings by patients (not just hospitals)
- [ ] Appointment booking
- [ ] Multilingual support (Hindi, Kannada, Telugu)

---

## 🧪 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Backend | Python, FastAPI, Uvicorn |
| Database | MySQL, SQLAlchemy |
| AI — Conversation | Groq API (LLaMA 3.3 70B) |
| AI — Specialist Detection | Sentence Transformers (all-MiniLM-L6-v2) |

---

## 📄 License

This project was built as an independent academic project at IIIT Raichur under the supervision of Dr. Kaushiki Roy, Assistant Professor, CSE Department.
---
 
> ⚠️ MediFind is not a substitute for professional medical advice, diagnosis or treatment. Always consult a qualified healthcare provider.
---

> ⚠️ MediFind is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.
