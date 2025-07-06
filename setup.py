"""creating a setup file to make the application executable."""
from setuptools import setup

setup(
    name='task-cli',
    version='0.1',
    py_modules=['app'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'task-cli=app:main',
        ],
    },
)
