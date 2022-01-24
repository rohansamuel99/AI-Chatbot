from tracemalloc import start
import webbrowser
import spacy
from training_ner import train_model
from spacy import displacy
from training_ner import train_model
from ticket_details import Ticket
from web_crawler import *
from weather import getweatherAt
import asyncio
nlp = spacy.load("en_core_web_md")
updated_nlp = spacy.load('/AI-Chatbot')


def require_details():
  print("Hello! Welcome to the chatbot feature. Nice to meet you")
  name = input("What is your name? \n")
  print(f"Hi, {name}. Nice to meet you!")
  userAnswering = True
  while userAnswering is True: 
    tripdestination = input("Where would you like to go? \n").lower()
      # More info grabbing here
    tripdestination = updated_nlp(tripdestination)
    for word in tripdestination.ents:
      # Testing to see if nlp has understood the the words and type of word inputted by user
      if word.label_ == "STATION":
        print("Just checking if you entered a station. Correct")
      else:
        return "you didn't enter in a station"
    tripdeparture = input ("From where will you be going? \n")
    tripdeparture = updated_nlp(tripdeparture)
    for a_word in tripdeparture.ents:
      if a_word.label_ == "STATION":
        print(f"Departure Station: {a_word.text}")
      else:
        return "you didn't enter in a station"
    # validation for time input
    departtime = input ("what time do you want to catch the train? \n")
    # validation for date input
    departdate = input ("And what date would you like to leave? \n")
    finishquestion = input("Is that everything? Type Y or N: ")
    if finishquestion == "Y" or "y":
      userAnswering = False
      # Create Ticket object and return instead of details_list
      aticket = Ticket(name,tripdestination,tripdeparture,departtime,departdate)

      ticketFares = crawl(aticket)

      count = 1
      print(f"Tickets found: ")
      print(f"Start   |   End   |   Time  |   Duration  |   Cost")
      for ticketFare in ticketFares.ticketFares:
        print(f"{count} {ticketFare.start} | {ticketFare.end} | {ticketFare.startTime} | {ticketFare.length} | £{ticketFare.cost}")
        count += 1

      print("")
      loop = asyncio.get_event_loop()
      loop.run_until_complete(getweatherAt(aticket))
      print("")

      buyTicketquestion = input("Would you like to purchase one of these tickets? Type Y or N: ")
      if buyTicketquestion == "Y" or "y":
        webbrowser.open(ticketFares.url)

      #N.B. need to sort ticketFares by cost using lamda
      #N.B. Remove the testing block from crawl() once require_details() works.

      return aticket
    else:
      userAnswering = True


async def getWeatherData(ticket):
  await getweatherAt(ticket)

def process_details(a_ticket):

  doc = updated_nlp(a_ticket.destination)
  doc2 = updated_nlp(a_ticket.departure_station)
  with doc.retokenize() as retokenizer:
    for ent in doc.ents:
      retokenizer.merge(doc[ent.start:ent.end])
      #print(ent.text)
  with doc2.retokenize() as retokenizer:
    for ent in doc2.ents:
      retokenizer.merge(doc2[ent.start:ent.end])
      #print(ent.text)

  return f"start = {a_ticket.departure_station}, finish = {a_ticket.destination}, day = {a_ticket.date_of_departure}, time = {a_ticket.time_of_departure}"
  # Return ticket object instead?
if __name__ == "__main__":
  pass