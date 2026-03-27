# 🤖 AI Resume Skill Gap Analyzer + Career Chatbot

An AI-powered full-stack application that analyzes resumes against job descriptions, identifies skill gaps, generates a personalized learning roadmap, and provides an intelligent career chatbot assistant.

---

## 📌 Features

### 🔍 Resume Analysis
- Upload resume (PDF)
- Compare with job description (JD)
- Extract skills using NLP
- Identify:
  - ✅ Matched skills
  - ❌ Missing skills
  - 📊 Skill match percentage

---

### 🧠 AI Intelligence Layer
- Skill normalization & mapping (e.g., Express.js → Express)
- Semantic skill expansion (MERN → React, Node.js, MongoDB)
- Resume signal analysis
- Skill depth estimation
- Confidence scoring

---

### 🛣️ Learning Roadmap Generator
- Phase-wise roadmap
- Skill priority mapping
- Estimated learning duration
- Structured growth plan

---

### 🤖 AI Career Chatbot
- Context-aware chatbot using resume analysis
- Powered by LLM (Groq API)
- Answers:
  - “Am I job ready?”
  - “Why is my score low?”
  - “What should I learn first?”
  - “Give me roadmap”
- Uses prompt engineering for accurate responses

---

### 🎨 Frontend (React)
- Modern dark UI 🌑
- Glassmorphism design
- Circular skill match indicator
- Skill tags & roadmap cards
- Charts (Recharts integration)

---

## 🛠️ Tech Stack

### 🔹 Frontend
- React (Vite)
- CSS
- Recharts

### 🔹 Backend
- FastAPI
- Python

### 🔹 AI / ML / NLP
- TF-IDF & similarity scoring
- Custom skill extraction pipeline
- LLM integration (Groq API)

---

# ⚙️ 🚀 How to Run the Project

## 🔹 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

pip install -r requirements.txt

GROQ_API_KEY=your_api_key_here

python -m src.api.app - run backend

Frontend Setup
cd frontend
npm install
npm run dev
