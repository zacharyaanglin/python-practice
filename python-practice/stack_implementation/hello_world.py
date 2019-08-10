from random import choice


class Person:
    def __init__(self, name):
        self.name = name
        self.greeting = "Hello {name}"


    def __str__(self):
        return self.make_greeting()

    def make_greeting(self):
        return self.greeting.format(name=self.name)


def main():
    people = [
        Person('Jake'),
        Person('Jill'),
        Person('BoB'),
    ]
    person = choice(people)
    print(person)


if __name__ == '__main__':
    main()

