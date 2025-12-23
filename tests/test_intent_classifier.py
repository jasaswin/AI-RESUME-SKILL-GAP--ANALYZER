from src.chatbot.intent_classifier import IntentClassifier

classifier = IntentClassifier()

questions = [
    "Am I job ready?",
    "Why is my match score low?",
    "What should I learn first?",
    "How long before I can apply?",
    "AWS vs Docker which is better?",
    "Hello"
]

for q in questions:
    intent = classifier.classify(q)
    print(f"Q: {q}")
    print(f"→ Intent: {intent}\n")
