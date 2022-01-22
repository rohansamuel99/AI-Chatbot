import spacy
from training_ner import train_model
from spacy import displacy
from training_ner import train_model
from ticket_details import Ticket
from web_crawler import crawl
nlp = spacy.load("en_core_web_md")
updated_nlp = spacy.load('C:\\Users\\Adam\\Desktop\\Adam Biggs\\Student\\University\\4. Year Three (2021-2022)\\Artificial Intelligence\\CSW-2\\AI-Chatbot') # Change to relative path or your own path


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
      # Testing to see if nlp has understood the words and type of word inputted by user
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
    departtime = input ("what time do you want to catch the train? \n")
    departdate = input ("And what date would you like to leave? \n")
    finishquestion = input("Is that everything? Type Y or N: ")
    if finishquestion == "Y" or "y":
      userAnswering = False
      # Create Ticket object and return instead of details_list
      aticket = Ticket(name,tripdestination,tripdeparture,departtime,departdate)

      tickets = crawl(aticket)



      return aticket
    else:
      userAnswering = True

def process_details(a_ticket):

  doc = updated_nlp(a_ticket.destination)
  doc2 = updated_nlp(a_ticket.departure_station)
  with doc.retokenize() as retokenizer:
    for ent in doc.ents:
      retokenizer.merge(doc[ent.start:ent.end])
      print(ent.text, ent.label_)
  with doc2.retokenize() as retokenizer:
    for ent in doc2.ents:
      retokenizer.merge(doc2[ent.start:ent.end])
      print(ent.text, ent.label_)

if __name__ == "__main__":
  pass