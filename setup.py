from setuptools import setup, find_packages

setup(
    name='simplechatbot',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'customtkinter',
        'chatterbot-corpus',
        'spacy',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz',
        'chatterbot @ git+https://github.com/ShoneGK/ChatterPy.git@main',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'simplechatbot=src.main:main',
        ],
    },
)
