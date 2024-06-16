from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class ChatModel(ChatBot):
    def __init__(self):
        super().__init__('Greeter')
        self._trainer = ChatterBotCorpusTrainer(self)
        self._trainer.train("chatterbot.corpus.english.greetings")

    def get_response(self, prompt: str) -> str:
        return super().get_response(prompt)
