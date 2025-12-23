from src.chatbot.chatbot import CareerChatbot


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

bot = CareerChatbot(analysis)

print(bot.chat("Am I job ready?"))
print(bot.chat("Why is my match score low?"))
print(bot.chat("What should I learn first?"))
print(bot.chat("How long before I can apply?"))
print(bot.chat("AWS vs Docker which is better?"))