from typing import Callable

class ChatModel:
    def __init__(self):
        self._response: Callable[[str], str] = lambda prompt: "Found 7" if '7' in prompt else "Not found"
    
    def get_response(self, prompt: str) -> str:
        return self._response(prompt)
