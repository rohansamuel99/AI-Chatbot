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
     # model = train_model()
     data = require_details()

     process_details(data)
     # print("Group 26 Chatbot :D")
