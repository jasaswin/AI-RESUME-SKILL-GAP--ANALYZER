from src.chatbot.intent_classifier import IntentClassifier
from src.chatbot.response_engine import CareerChatbot


class ChatbotEngine:
    """
    Orchestrates intent classification and response generation
    """

    def __init__(self, analysis: dict):
        self.intent_classifier = IntentClassifier()
        self.chatbot = CareerChatbot(analysis)

    def ask(self, question: str) -> str:
        intent = self.intent_classifier.classify(question)
        response = self.chatbot.respond(intent, question)
        return response
