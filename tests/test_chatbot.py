from src.chatbot.chatbot import CareerChatbot

analysis_context = {
    "career_readiness": {
        "readiness_level": "Trainable",
        "hiring_signal": "Needs upskilling"
    },
    "gaps": {
        "missing_optional_skills": ["docker", "aws"]
    },
    "priority_map": {
        "high_priority": ["docker"]
    },
    "roadmap": [
        {"skill": "docker", "estimated_weeks": 6}
    ]
}

bot = CareerChatbot(analysis_context)
print(bot.chat("Am I job ready?"))
print(bot.chat("Why is my match score low?"))
print(bot.chat("What should I learn first?"))
print(bot.chat("How long before I can apply?"))
print(bot.chat("AWS vs Docker which is better?"))

