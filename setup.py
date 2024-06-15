from setuptools import setup, find_packages

setup(
    name='simplechatbot',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'customtkinter',
    ],
    entry_points={
        'console_scripts': [
            'mychatapp=src.main:main',
        ],
    },
)