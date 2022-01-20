from random import choice
from experta import *

class Greet():
    name = Field(str)
    location = Field(str)
    departure = Field(str)
    leave_time = Field(str)
    arrive_time= Field(str)
    date = Field(int)
    month = Field(str)



class Conversation(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")


    @Rule(Fact(action='greet'), NOT (Fact(name=W())))
    def ask_name(self):
        self.declare(Fact(name=input("Hello, nice to meet you. What is your name? \n")))

    @Rule(Fact(action='greet'), AS.n << (Fact(name='')))
    def ask_name_error(self,n):
            self.retract(n)# How to remove previous empty string fact
            self.declare(Fact(name = input("You didn't enter in your name \n")))

    @Rule(Fact(action='greet'), NOT (Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("Where do you want to go? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(departure=W)))
    def ask_departure_station(self):
        self.declare(Fact(departure=input("What station will you be leaving from? \n")))

    @Rule(Fact(action='greet'), NOT(Fact(date_of_departure=W)))# Has to be numbers: 1 -31. account for months less than 31
    def ask_date_of_departure(self):
        self.declare(Fact(date_of_departure = input("What day would you like to leave? ")))
    # Rule for if they enter a day mon-sun

    @Rule(Fact(action='greet'), NOT(Fact(month_of_departure=W))) # Jan - Dec
    def ask_month_of_departure(self):
        self.declare(Fact(month_of_departure=input("What month would you like to leave? ")))

    @Rule(Fact(action='greet'), NOT (Fact(leave_time=W)))
    # 24hr format 4 digits
    def ask_leaving_time(self):
        self.declare(Fact(leave_time=input("What time do you want to leave? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(arrive_time=W)))
    def ask_arrive_time(self):
        self.declare(Fact(arrive_time=input("And what time would you like to arrive? \n")))


    # Rule for if they want a return ticket

    @Rule(Fact(action='greet'),
        Fact(name= MATCH.name),
        Fact(location = MATCH.location),
        Fact(departure= MATCH.departure),
        Fact(leave_time = MATCH.time),
        Fact(date_of_departure = MATCH.date),
        Fact(month_of_departure = MATCH.month),
        (Fact(arrive_time = MATCH.arrivetime)))

    def greet(self,name,location,departure,time,arrivetime, date, month):
        print(f"Hi {name}, so you want to go to {location},"
              f"leaving from {departure} station. You want to leave at {time}  on the {date} of {month} and arrive at {arrivetime}?")

'''
    @Rule(Fact(action='greet'),
          Fact(name=MATCH.name),
          Fact(location=MATCH.location),
          Fact(departure=MATCH.departure),
          Fact(leave_time=MATCH.time),
          NOT(Fact(arrive_time=MATCH.arrivetime))
    def need_arrive_time(self, name, location,departure,time):
        print("please enter your arrival time")
        # go back to start or trigger input for arrival time
        # self.declare(arrive_time) = input("please enter arrival time")
'''



if __name__ == "__main__":
    engine = Conversation()
    engine.reset()
    engine.run()
