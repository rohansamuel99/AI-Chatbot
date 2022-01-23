import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import pandas as pd
import random
import warnings
from nlpu import require_details, process_details
from training_ner import train_model
from web_crawler import crawl
import webbrowser
nlp = spacy.load("en_core_web_md")
updated_nlp = spacy.load('/AI-Chatbot')

if __name__ == "__main__":
     #model = train_model()
     data = require_details()
     ticketFares = crawl(data)

     #N.B. need to sort ticketFares by cost using lamda
     #N.B. Remove the testing block from crawl() once require_details() works.

     webbrowser.open(ticketFares.url)

     process_details(data)
     # print("Group 26 Chatbot :D")
