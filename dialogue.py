from random import choice
from experta import *

class Conversation(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")

    @Rule(Fact(action='greet'), NOT (Fact(name=W())))
    def ask_name(self):
        self.declare(Fact(name=input("Hello, nice to meet you. What is your name? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("Where do you want to go? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(departure=W)))
    def ask_departure_station(self):
        self.declare(Fact(departure=input("What station will you be leaving from? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(time=W)))
    def ask_leaving_time(self):
        self.declare(Fact(time=input("What time do you want to leave? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(arrivetime=W)))
    def ask_arrive_time(self):
        self.declare(Fact(time=input("And what time would you like to arrive? \n")))


    # Rule for if they want a return ticket

    @Rule(Fact(action='greet'),
        Fact(name= MATCH.name),
        Fact(location = MATCH.location),
        Fact(departure= MATCH.departure),
        Fact(time = MATCH.time),
        Fact(arrivetime = MATCH.arrivetime))

    def greet(self,name,location,departure,time,arrivetime):
        print(f"Hi {self.name}, so you want to go to {self.name},"
              f"leaving from {self.departure} station. You want to leave at {self.time} and arrive at {self.arrivetime}?")


