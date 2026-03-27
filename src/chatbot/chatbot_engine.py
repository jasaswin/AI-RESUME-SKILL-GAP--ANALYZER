# from src.chatbot.intent_classifier import IntentClassifier
# from src.chatbot.chatbot import CareerChatbot


# class ChatbotEngine:
#     """
#     Orchestrates intent classification and response generation
#     """

#     def __init__(self, analysis: dict):
#         self.intent_classifier = IntentClassifier()
#         self.chatbot = CareerChatbot(analysis)

#     def ask(self, question: str) -> str:
#         intent = self.intent_classifier.classify(question)
#         # response = self.chatbot.respond(intent, question)
#         response = self.chatbot.chat(question)
#         return response


from src.chatbot.chatbot import CareerChatbot


class ChatbotEngine:
    def __init__(self, analysis: dict):
        self.chatbot = CareerChatbot(analysis)

    def ask(self, question: str) -> str:
        return self.chatbot.chat(question)