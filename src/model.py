from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.storage import SQLStorageAdapter

class ChatModel(ChatBot):
    def __init__(self):
        super().__init__('Greeter')
        if not SQLStorageAdapter().count():
            trainer = ChatterBotCorpusTrainer(self)
            trainer.train("chatterbot.corpus.english.food")
            trainer.train("chatterbot.corpus.english.greetings")
            trainer.train("chatterbot.corpus.english.conversations")
            trainer.train("chatterbot.corpus.english.emotion")

    def get_casual_response(self, prompt: str) -> str:
        return super().get_response(prompt)
