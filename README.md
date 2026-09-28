# 🤖 AI Resume Skill Gap Analyzer + Career Chatbot

An AI-powered full-stack application that analyzes resumes against job descriptions, identifies skill gaps, generates a personalized learning roadmap, and provides an intelligent AI career chatbot.

---

## 🌐 Live Demo

🚀 **Live Application:**  
https://ai-resume-skill-gap-analyzer-fnd.vercel.app/

🔗 **Backend API:**  
https://ai-resume-skill-gap-analyzer-api.onrender.com/

📚 **Swagger API Documentation:**  
https://ai-resume-skill-gap-analyzer-api.onrender.com/docs

💻 **GitHub Repository:**  
https://github.com/jasaswin/AI-RESUME-SKILL-GAP--ANALYZER

---

# 📌 Overview

The **AI Resume Skill Gap Analyzer** helps job seekers understand how well their resume matches a target job description.

The application analyzes a resume and job description, identifies matching and missing skills, calculates a skill-match percentage, generates a personalized learning roadmap, and provides an AI-powered career chatbot.

---

# ✨ Features

## 🔍 Resume Analysis

- Upload resume in PDF format
- Enter a target job description
- Extract relevant skills
- Compare resume skills with job requirements
- Identify matched skills
- Identify missing skills
- Calculate skill match percentage

---

## 🧠 AI Intelligence Layer

The application uses NLP and AI techniques to improve resume analysis.

### Skill Normalization

Examples:

```text
Express.js → Express
ReactJS → React
NodeJS → Node.js
Semantic Skill Expansion

For example:

MERN
 ├── MongoDB
 ├── Express
 ├── React
 └── Node.js

This allows related technologies to be considered during skill matching.

📊 Skill Gap Analysis

The application compares the candidate's skills with the skills required by the job description.

Example:

Skill	Status
Java	✅ Matched
SQL	✅ Matched
Spring Boot	❌ Missing
AWS	❌ Missing
Git	✅ Matched
🛣️ Personalized Learning Roadmap

The system generates a structured learning roadmap based on the identified skill gaps.

The roadmap can include:

Skills to learn
Skill priority
Learning phases
Estimated learning duration
Recommended learning sequence

Example:

Phase 1
 ├── Java Fundamentals
 └── OOP

Phase 2
 ├── Spring Boot
 └── REST APIs

Phase 3
 ├── SQL
 └── Database Integration

Phase 4
 └── AWS Fundamentals
🤖 AI Career Chatbot

The application provides an AI-powered career assistant.

Example questions:

Am I job ready?

Why is my score low?

What should I learn first?

Give me a roadmap.

How can I improve my resume?

How can I learn AWS?

The chatbot uses the Groq API and an LLM to generate career-related responses.

🎨 Frontend

The application includes a modern dark-themed interface with:

🌑 Dark UI
✨ Glassmorphism design
📊 Skill match visualization
🏷️ Skill tags
📚 Roadmap cards
📈 Charts
🤖 AI chatbot
📱 Responsive layout
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
CSS
Axios
React Router
Recharts
Backend
Python
FastAPI
Uvicorn
Pydantic
AI / ML / NLP
TF-IDF
Cosine Similarity
NLP-based skill extraction
Skill normalization
Semantic skill expansion
Groq LLM
PDF Processing
pdfplumber
Deployment
Vercel — Frontend
Render — Backend
Version Control
Git
GitHub
📂 Project Structure
AI-RESUME-SKILL-GAP--ANALYZER/
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │
│   │   ├── components/
│   │   │   ├── Chatbot.jsx
│   │   │   ├── SkillChart.jsx
│   │   │   ├── SkillMatchCard.jsx
│   │   │   ├── UploadResume.jsx
│   │   │   ├── gaplist.jsx
│   │   │   └── roadmapview.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── home.jsx
│   │   │   └── result.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── src/
│   ├── api/
│   │   ├── app.py
│   │   └── routes.py
│   │
│   ├── llm/
│   │   └── llm_formatter.py
│   │
│   ├── utils/
│   │   └── pdf_reader.py
│   │
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Setup & Running Locally

Follow the steps below to run the project locally.

1. Prerequisites

Make sure the following are installed on your system:

Python 3.10+
Node.js 18+
npm
Git

Check your versions:

python --version
node --version
npm --version
git --version
2. Clone the Repository

Open a terminal and run:

git clone https://github.com/jasaswin/AI-RESUME-SKILL-GAP--ANALYZER.git

Move into the project:

cd AI-RESUME-SKILL-GAP--ANALYZER
3. Backend Setup

The backend is built using FastAPI and Python.

Step 3.1 — Create a Virtual Environment

From the project root:

Windows
python -m venv venv

Activate the virtual environment:

venv\Scripts\activate

You should see something similar to:

(venv) PS C:\...\AI-RESUME-SKILL-GAP--ANALYZER>
macOS / Linux
python3 -m venv venv

Activate it:

source venv/bin/activate
4. Install Backend Dependencies

Make sure the virtual environment is activated.

Run:

pip install -r requirements.txt

This installs the required Python packages including:

FastAPI
Uvicorn
Groq
pdfplumber
scikit-learn
pandas
numpy
python-dotenv
python-multipart
5. Configure Groq API Key

The chatbot requires a Groq API key.

Create a file named:

.env

in the project root:

AI-RESUME-SKILL-GAP--ANALYZER/
│
├── .env
├── requirements.txt
├── src/
└── frontend/

Add:

GROQ_API_KEY=your_groq_api_key_here

Replace:

your_groq_api_key_here

with your actual Groq API key.

Important

Do not upload your .env file to GitHub.

Your .gitignore should contain:

.env
venv/
__pycache__/
node_modules/
dist/
6. Run the Backend

From the project root, with the virtual environment activated:

uvicorn src.api.app:app --reload

The backend should start at:

http://127.0.0.1:8000

You should see something similar to:

Uvicorn running on http://127.0.0.1:8000
7. Test the Backend

Open the following URL in your browser:

http://127.0.0.1:8000

You can also open the FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

Swagger allows you to test the API endpoints directly.

Available endpoints:

GET  /
POST /analyze/
POST /chat
8. Frontend Setup

Open a new terminal.

Keep the backend terminal running.

Move into the frontend folder:

cd frontend

Install the Node.js dependencies:

npm install
9. Configure Frontend API

The frontend communicates with the FastAPI backend through Axios.

The API configuration is located at:

frontend/src/services/api.js

For local development, the API base URL should point to:

http://127.0.0.1:8000

Example:

import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const analyzeResume = (formData) =>
  API.post("/analyze/", formData);

export const chatWithBot = (data) =>
  API.post("/chat", data);
10. Run the Frontend

Inside the frontend directory:

npm run dev

Vite will start the development server.

Usually the application will be available at:

http://localhost:5173

Open that URL in your browser.

▶️ Running the Complete Application

You need two terminals running at the same time.

Terminal 1 — Backend

From the project root:

venv\Scripts\activate
uvicorn src.api.app:app --reload

Backend:

http://127.0.0.1:8000
Terminal 2 — Frontend

From the project root:

cd frontend
npm run dev

Frontend:

http://localhost:5173
🔄 Application Flow
                 USER
                   │
                   ▼
          ┌─────────────────┐
          │ React Frontend  │
          │     Vite        │
          └────────┬────────┘
                   │
                   │ HTTP Request
                   ▼
          ┌─────────────────┐
          │ FastAPI Backend │
          └────────┬────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
   Resume Processing   Job Description
          │                 │
          └────────┬────────┘
                   ▼
          ┌─────────────────┐
          │ NLP / Skill     │
          │ Analysis        │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Skill Gap       │
          │ Analysis        │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Learning        │
          │ Roadmap         │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ React Results   │
          │ Dashboard       │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ AI Career       │
          │ Chatbot         │
          └────────┬────────┘
                   │
                   ▼
             Groq LLM API
🔌 API Endpoints
Root Endpoint
GET /

Used to check whether the backend is running.

Resume Analysis
POST /analyze/

This endpoint processes:

Resume PDF
Job description

and returns the skill analysis.

Career Chatbot
POST /chat

Example request:

{
  "question": "How should I learn AWS?",
  "analysis": {}
}

Example response:

{
  "answer": "Here’s a quick roadmap to get started with AWS..."
}
🌐 Production Deployment

The application is deployed using two separate services.

Frontend — Vercel

Live application:

https://ai-resume-skill-gap-analyzer-fnd.vercel.app/

The React/Vite frontend is hosted on Vercel.

Backend — Render

Backend:

https://ai-resume-skill-gap-analyzer-api.onrender.com/

Swagger:

https://ai-resume-skill-gap-analyzer-api.onrender.com/docs

The FastAPI backend is hosted on Render.

🔐 Production Environment Variables

For the deployed backend, configure the following environment variable in Render:

GROQ_API_KEY

Value:

your_groq_api_key

The API key should never be exposed in frontend code.

🧪 Testing

The backend can be tested using:

FastAPI Swagger
Postman
Frontend application

Swagger:

https://ai-resume-skill-gap-analyzer-api.onrender.com/docs

Test Chatbot

Use:

{
  "question": "How can I learn AWS?",
  "analysis": {}
}

Expected response:

{
  "answer": "..."
}
🚀 Production Workflow
GitHub
   │
   ├──────────────► Vercel
   │                  │
   │                  ▼
   │             React Frontend
   │
   └──────────────► Render
                      │
                      ▼
                 FastAPI Backend
                      │
                      ▼
                  Groq API
