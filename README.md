# Simple Recommendation Chatbot

This project is a simple recommendation chatbot that can suggest recipes based on user input. It's built in Python and uses a predefined set of recipes.

## Features

- Recommend a recipe based on user input
- Provide alternatives if the user wants something different
- Store the recipe for future reference

## Installation

This project uses setuptools for packaging and distribution. It was tested only on Python 3.9.0. Here's how you can install it:

1. Make sure your current version of Python is 3.9.0
```bash
python --version
```

2. Clone the repository:
```bash
git clone https://github.com/iendjei0/simple-recommendation-chatbot
```

3. Navigate to the project directory:
```bash
cd simple-recommendation-chatbot
```

4. Install the package:
```bash
python setup.py install
```

## Launching
After installing the package, you can launch the chatbot from the command line like this:
```bash
simplechatbot
```

## Testing
This project uses pytest for testing. After installing the package, you can run the tests like this:
```bash
simplechatbot test
```