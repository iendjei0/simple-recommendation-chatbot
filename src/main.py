from src.controller import ChatController
from sys import argv

def main():
    if len(argv) > 1 and argv[1] == 'test':
        import pytest
        pytest.main(['-v', 'src/test/test.py'])
    else:
        ChatController().run()

if __name__ == "__main__":
    main()