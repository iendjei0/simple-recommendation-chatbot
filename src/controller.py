from src.model import ChatModel
from src.view import ChatView

class ChatController():
    def __init__(self):
        self._model = ChatModel()
        self._view = ChatView()
    def run(self) -> None:
        self._view.mainloop()