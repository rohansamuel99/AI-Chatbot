from random import choice
from experta import *
import datetime
from nlpu import require_details
from ticket_details import Ticket
import re

class Greet(Fact):
    pass

class name(Fact):
    name = Field(str)

    def __str__(self):
        return f"{name}"

class destination(Fact):
    destination = Field(str)


class departing_station(Fact):
    departure = Field(str)


class leave_time(Fact):
    leave_time = Field(str)


class arrive_time(Fact):
    arrive_time = Field(int)


class date(Fact):
    date = Field(str)


class month(Fact):
    month = Field(str)


class ValidAnswer(Fact):
    answer = Field(int, mandatory=True)

class validations(Fact):
    dateinput = Field(str)
    def regex_match(self,dateinput):
        if (re.match(r'[a-zA-Z]',str(dateinput))):
            return "True"
        else:
            return "invalid entry. Use 1-31"

class Conversation(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")



    @Rule(Fact(action='greet'), AS.n << (name(name =W())), salience = 8)
    def ask_name(self,n):
            self.declare(name(n))
            print(".....Name retrieved......")

    @Rule(Fact(action='greet'), AS.n << (name(name='')),salience=7)
    def ask_name_error(self,n):
            self.retract(n)# How to remove previous empty string fact
            self.declare(name(name = input("You didn't enter in your name \n")))

    @Rule(Fact(action='greet'),  (destination(destination=W())), salience=7)
    def ask_location(self):
        self.declare(destination(destination))
        print("......Destination retrieved.......")


    @Rule(Fact(action='greet'),  (departing_station(departure=W())),salience=6)
    def ask_departure_station(self):
        #self.declare(departing_station(departure=W()))
        print(f"departing station: {departing_station}")
    @Rule(Fact(action='greet'), (date(date= MATCH.answer)),salience=5)
    def ask_date_of_departure(self):
        #self.declare(date(date = input("What day would you like to leave? Enter number 1-31 \n ")))
        print(".....Date Retrieved........")

    # Rule for if they enter a day mon-sun

    @Rule(Fact(action='greet'), AS.date << (date(date_of_departure=L('31'))),salience=4)  # Has to be numbers: 1 -31. don't forget to take into account for months less than 31 days
    def ask_date_error(self,date):
        self.declare(date(date_of_departure=input("You entered incorrectly. Please try again \n ")))
        print("incorrect date")
    # Rule for if they enter a day mon-sun



    @Rule(Fact(action='greet'), (month(month_of_departure=W())),salience=3) # Jan - Dec
    def ask_month_of_departure(self):
        #self.declare(month(month_of_departure=input("What month would you like to leave? ")))
        print("hi")
    @Rule(Fact(action='greet'),  (leave_time(leave_time=W())),salience=2)
    # 24hr format 4 digits
    def ask_leaving_time(self):
        #self.declare(leave_time(leave_time=input("What time do you want to leave? \n")))
        print(".....leaving time retrieved.......")
    @Rule(Fact(action='greet'), NOT (arrive_time(arrive_time=W())),salience =1)
    def ask_arrive_time(self):
        #self.declare(arrive_time(arrive_time=input("And what time would you like to arrive? \n")))
        print(".....arriving time retrieved.....")

    # Rule for if they want a return ticket

    def invoke_web_scraping(self,name,destination,departure,time,arrivetime,date,month):
        pass
        # Call webscraping





if __name__ == "__main__":
    a_ticket = require_details()
    engine = Conversation()
    engine.reset()
    engine.declare(name(name=str(a_ticket.name)),
                   destination(destination =str(a_ticket.destination)),
                   departing_station(departure =str(a_ticket.departure_station)),
                   leave_time(leave_time = str(a_ticket.time_of_departure)),
                   date(date = str(a_ticket.date_of_departure)))
    engine.facts
    engine.run()
