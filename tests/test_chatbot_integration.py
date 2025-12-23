from src.chatbot.chatbot_engine import ChatbotEngine

analysis = {
    "career_readiness": {
        "readiness_level": "Trainable",
        "hiring_signal": "Needs targeted upskilling"
    },
    "gaps": {
        "missing_core_skills": [],
        "missing_optional_skills": ["aws", "docker"]
    },
    "priority_map": {
        "high_priority": ["docker", "aws"],
        "medium_priority": [],
        "low_priority": []
    },
    "roadmap": [
        {"skill": "docker", "estimated_weeks": 5.8},
        {"skill": "aws", "estimated_weeks": 5.8}
    ]
}

bot = ChatbotEngine(analysis)

questions = [
    "Am I job ready?",
    "Why is my match score low?",
    "What should I learn first?",
    "How long before I can apply?",
    "AWS vs Docker which is better?"
]

for q in questions:
    print(f"\nUser: {q}")
    print("Bot:", bot.ask(q))
