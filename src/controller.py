from model import ChatModel
from view import ChatView

class ChatController():
    def __init__(self):
        self._model = ChatModel()
        self._view = ChatView(self)

    def run(self) -> None:
        self._view.mainloop()

    def button_press(self) -> None:
        prompt = self._view.get_user_text()
        result = self._model.make_it_louder(prompt)
        print(result)