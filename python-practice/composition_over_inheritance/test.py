import abc
from typing import List

class Name:

    def __init__(self, *args: str):
        self.names: str = ' '.join(args)
        self.first = ''
        if self.names.strip():
            self.first: str = args[0]
        try:
            self.last: str = args[-1]
        except IndexError:
            self.last: str = ''


class Person(abc.ABC):

    @abc.abstractstaticmethod
    def talk(words: List[str]) -> None:
        pass
        

class Anglin(Person):

    def __init__(self, name: Name):
        self.name = Name
        self.last = 'Anglin'
    
    @staticmethod
    def talk(words: List[str]) -> None:
        print("Hi there!")
        print(words)
        print("Goodbye!")
