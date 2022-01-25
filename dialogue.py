# -------------------------
# File: dialogue.py
# Classes: Conversation,CustomerService, Knowledge, Greet, name, destination, departing_station, leave_time, arrive_time, ValidAnswer,validations, train, person_position, delayed_time_train, where_train_is_going
# Notes: This file is used to control the dialogue. NlPU feeds this file facts and dialogue has rules that execute if the rules match the fafcts
# Author: Samuel Bedeau
# -------------------------

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
# Fact base for Task 2 - Improving Customer Service
class train(Fact):
    which_train = Field(str)
class person_position(Fact):
    where_is_person_at = Field(str)

class delayed_time_train(Fact):
    delayed = Field(str)
class where_train_is_going(Fact):
    train_destination = Field(str)

class Conversation():

    @Rule(Fact(action='greet'), AS.n << (name(name =W())), salience = 15)
    def ask_name(self,n):
            self.declare(name(n))
            print(".....Name retrieved......")

    @Rule(Fact(action='greet'), AS.n << (name(name='')),salience=14)
    def ask_name_error(self,n):
            self.retract(n)# How to remove previous empty string fact
            self.declare(name(name = input("You didn't enter in your name \n")))

    @Rule(Fact(action='greet'),  (destination(destination=W())), salience=13)
    def ask_location(self):
        self.declare(destination(destination))
        print("......Destination retrieved.......")


    @Rule(Fact(action='greet'),  (departing_station(departure =W())),salience=12)
    def ask_departure_station(self):
        #self.declare(departing_station(departure=W()))
        print("....Departing Station retrieved......")

    @Rule(Fact(action='greet'), NOT(date(date=W())),salience=11)
    def ask_date_of_departure(self):
        #self.declare(date(date = input("What day would you like to leave? Enter number 1-31 \n ")))
        print(".....Date Retrieved........")

    @Rule(Fact(action='greet'), AS.date << (date(date=L('31'))),salience=10)  # Has to be numbers: 1 -31. don't forget to take into account for months less than 31 days
    def ask_date_error(self,date):
        self.declare(date(date=input("You entered incorrectly. Please try again \n ")))
        print("incorrect date")

    @Rule(Fact(action='greet'), (month(month_of_departure=W())),salience=9) # Jan - Dec
    def ask_month_of_departure(self):
        #self.declare(month(month_of_departure=input("What month would you like to leave? ")))
        print(".....Month of Departure retrieved......")

    @Rule(Fact(action='greet'), (leave_time(leave_time=W())),salience=8)
    # 24hr format 4 digits
    def ask_leaving_time(self):
        #self.declare(leave_time(leave_time=input("What time do you want to leave? \n")))
        print(".....leaving time retrieved.......")

    @Rule(Fact(action='greet'), NOT (arrive_time(arrive_time=W())),salience =7)
    def ask_arrive_time(self):
        #self.declare(arrive_time(arrive_time=input("And what time would you like to arrive? \n")))
        print(".....arriving time retrieved.....")

    # Rule for if they want a return ticket

    @Rule(Fact(action='greet'),
          NOT (name(name=MATCH.name),
          NOT (destination(destination=MATCH.destination),
          NOT (departing_station(departure= MATCH.departure),
          NOT (date(date=MATCH.date),
          NOT (leave_time(leave_time=MATCH.leave_time))
          )))))
    def greeting(self,name,destination,departure,date,leave_time):
        print(f"Hi {name}, so you are going to {destination} from {departure}, and leaving at {leave_time} on {date}?")
    def invoke_web_scraping(self,name,destination,departure,time,arrivetime,date,month):
        pass
        # Call webscraping




class CustomerService():
    @Rule(Fact(action='ask'), NOT (train(which_train=W())),salience = 6)
    def retrieve_which_train(self):
        self.declare(train(which_train = input("What train are you on?")))

    @Rule(Fact(action='ask'), NOT (person_position(where_is_person_at=W())),salience=5)
    def retrieve_where_is_train(self):
        self.declare(person_position(where_is_train=input("Where are you currently waiting for the train? Input Station")))

    @Rule(Fact(action='ask'), NOT (delayed_time_train(delayed=W())),salience=4)
    def retrieve_delay_time(self):
        self.declare(delayed_time_train(delayed=input("How long is the train delayed for?")))


    @Rule(Fact(action='ask'), NOT (where_train_is_going(train_destination=W())), salience=3)
    def retrieve_train_destination(self):
        self.declare(where_train_is_going(train_destination=input("And where is the train going?")))

    @Rule(Fact(action='ask'),
      NOT (train(which_train= MATCH.which_train),
      NOT (person_position(where_is_person_at = MATCH.where_is_person_at),
      NOT (delayed_time_train(delayed= MATCH.delayed),
      NOT (where_train_is_going(train_destination = MATCH.train_destination))))))
    def predictive_modelling(self):
        print("test")


class Knowledge(Conversation,CustomerService,KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield (Fact(action="ask"))
        yield Fact(action="greet")

if __name__ == "__main__":
    a_ticket = require_details()
    engine = Knowledge()
    engine.reset()
    engine.declare(name(name=str(a_ticket.name)),
                   destination(destination =str(a_ticket.destination)),
                   departing_station(departure =str(a_ticket.departure_station)),
                   leave_time(leave_time = str(a_ticket.time_of_departure)),
                   date(date = str(a_ticket.date_of_departure)))
    engine.facts
    engine.run()
