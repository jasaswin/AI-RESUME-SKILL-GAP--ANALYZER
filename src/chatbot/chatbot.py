from src.chatbot.intent_classifier import IntentClassifier
from src.chatbot.response_engine import ResponseEngine


class CareerChatbot:
    """
    Public chatbot interface
    """

    def __init__(self, analysis_context: dict):
        self.context = analysis_context
        self.intent_classifier = IntentClassifier()
        self.response_engine = ResponseEngine()

    def chat(self, user_query: str) -> str:
        intent = self.intent_classifier.classify(user_query)

        return self.response_engine.respond(
            intent=intent,
            analysis=self.context,
            question=user_query
        )
