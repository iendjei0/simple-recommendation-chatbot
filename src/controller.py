from model import ChatModel
from view import ChatView

class ChatController():
    def __init__(self):
        self._model = ChatModel()
        self._view = ChatView()
    def run(self) -> None:
        while True:
            prompt = input("Prompt: ")
            if prompt in ["exit", "quit", "q"]:
                break
            response = self._model.get_response(prompt)
            self._view.show_text(response)