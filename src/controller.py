from src.model import ChatModel
from src.view import ChatView

class ChatController():
    def __init__(self):
        self._model = ChatModel()
        self._view = ChatView(self)

    def run(self) -> None:
        self._view.mainloop()

    def button_press(self) -> None:
        prompt = self._view.get_user_text()
        result = self._model.get_response(prompt)
        self._view.add_chat_text(f"{self._view.username}: {prompt}\n{self._view.botname}: {result}\n")
        self._view.set_user_text("")
        self._view.scroll_chat_down()