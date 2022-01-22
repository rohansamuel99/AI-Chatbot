from random import choice
from experta import *
import datetime
import re

class Greet(Fact):
    name = Field(str)
    destination = Field(str)
    departure = Field(str)
    leave_time = Field(int)
    arrive_time= Field(int)
    date = Field(int)
    month = Field(str)


class validations(Fact):
    def regex_match(self):
        dateinput = Field(str)
        if (re.match(r'[a-zA-Z]',str(dateinput))):
            return "True"
        else:
            return "invalid entry. Use 1-31"



class Conversation(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")



    @Rule(Fact(action='greet'), NOT (Fact(name=W())), salience =8)
    def ask_name(self):
        self.declare(Fact(name=input("Hello, nice to meet you. What is your name? \n")))

    @Rule(Fact(action='greet'), AS.n << (Fact(name='')),salience=7)
    def ask_name_error(self,n):
            self.retract(n)# How to remove previous empty string fact
            self.declare(Fact(name = input("You didn't enter in your name \n")))

    @Rule(Fact(action='greet'), NOT (Fact(destination=W())), salience=7)
    def ask_location(self):
        self.declare(Fact(destination=input("Where do you want to go? \n")))


    @Rule(Fact(action='greet'), NOT (Fact(departure=W())),salience=6)
    def ask_departure_station(self):
        self.declare(Fact(departure=input("What station will you be leaving from? \n")))

    @Rule(Fact(action='greet'), NOT(Greet(date= MATCH.date_of_departure)),salience=5)
    #@Rule(Fact(action='greet'), NOT (Fact(date=P(lambda p: 1 <= p <= 31))),salience=5) # Has to be numbers: 1 -31. don't forget to take into account for months less than 31 days
    #@Rule(Fact(action='greet'),NOT (validations(date=P(lambda p: 1<= p <=31))), salience=5)
    def ask_date_of_departure(self):
        self.declare(Fact(date_of_departure = input("What day would you like to leave? Enter number 1-31 \n ")))


    # Rule for if they enter a day mon-sun

    @Rule(Fact(action='greet'), AS.date << (Fact(date_of_departure=L('31'))),salience=4)  # Has to be numbers: 1 -31. don't forget to take into account for months less than 31 days
    def ask_date_error(self,date):
        self.declare(Fact(date_of_departure=input("You entered incorrectly. Please try again \n ")))

    # Rule for if they enter a day mon-sun



    @Rule(Fact(action='greet'), NOT(Fact(month_of_departure=W())),salience=3) # Jan - Dec
    def ask_month_of_departure(self):
        self.declare(Fact(month_of_departure=input("What month would you like to leave? ")))

    @Rule(Fact(action='greet'), NOT (Fact(leave_time=W())),salience=2)
    # 24hr format 4 digits
    def ask_leaving_time(self):
        self.declare(Fact(leave_time=input("What time do you want to leave? \n")))

    @Rule(Fact(action='greet'), NOT (Fact(arrive_time=W())),salience =1)
    def ask_arrive_time(self):
        self.declare(Fact(arrive_time=input("And what time would you like to arrive? \n")))


    # Rule for if they want a return ticket

    @Rule(Fact(action='greet'),
        Fact(name= MATCH.name),
        Fact(destination = MATCH.destination),
        Fact(departure= MATCH.departure),
        Fact(leave_time = MATCH.time),
        Fact(date_of_departure = MATCH.date),
        Fact(month_of_departure = MATCH.month),
        (Fact(arrive_time = MATCH.arrivetime)))

    def greet(self,name,destination,departure,time,arrivetime, date, month):
        print(f"Hi {name}, so you want to go to {destination},"
              f"leaving from {departure} station. You want to leave at {time}  on the {date} of {month} and arrive at {arrivetime}?")

    def invoke_web_scraping(self,name,destination,departure,time,arrivetime,date,month):
        pass
        # Call webscraping





if __name__ == "__main__":
    engine = Conversation()
    engine.reset()
    print(engine.facts)
    engine.run()
