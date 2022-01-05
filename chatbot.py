import spacy
import nltk
from spacy import displacy
nlp = spacy.load("en_core_web_md")

class UserDetails:
  def __init__(self, name, destination, departure_station,time_of_departure,date_of_departure):
    self.name = name
    self.destination = destination
    self.departure_station = departure_station
    self.time_of_departure = time_of_departure
    self.date_of_departure = date_of_departure

def process_details(data):
  # Nltk tagging for words 
  # Do entities instead 
  sentence = ' '.join([str(item) for item in data])
  words = nltk.word_tokenize(sentence)
  pos_tagged = nltk.pos_tag(words)
  ne_tagged = nltk.ne_chunk(pos_tagged)
  print("NE tagged text:")
  print(ne_tagged)
  print()
  print("Recognized named entities:")
  for ne in ne_tagged:
      if hasattr(ne, "label"):
          print(ne.label(), ne[0:])



def require_details():
  details_list = []
  print("Hello! Welcome to the chatbot feature. Nice to meet you")
  name = input("What is your name? \n")
  print(f"Hi, {name}. Nice to meet you!")
  userAnswering = True
  while userAnswering is True: 
    tripdestination = input("Where would you like to go? \n")
      # More info grabbing here
    tripdestination = nlp(tripdestination)
    for word in tripdestination.ents:
      # Testing to see if nlp has understood the the words and type of word inputted by user
      if word.label_ == "GPE":
        print("Just checking if you entered a city. Correct") 
      else:
        return "you didn't enter in a city"
    tripdeparture = input ("From where will you be going? \n")
    tripdeparture = nlp(tripdeparture)
    for a_word in tripdeparture.ents:
      if a_word.label_ == "GPE":
        print(f"Departure: {a_word.text}")
      else:
        return "you didn't enter in a city"
    departtime = input ("what time do you want to catch the train? \n")
    departdate = input ("And what date would you like to leave? \n")
    finishquestion = input("Is that everything? Type Y or N: ")
    if finishquestion == "Y":
      userAnswering = False
      details_list.append(name)
      details_list.append(tripdestination)
      details_list.append(tripdeparture)
      details_list.append(departtime)
      details_list.append(departdate)
      return details_list
    else:
      userAnswering = True

if __name__ == "__main__":
  '''
  name, tripdestination, tripdeparture, departtime, departdate = require_details()
  user = UserDetails(name, tripdestination, tripdeparture, departtime, departdate, require_details)

'''