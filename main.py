import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import pandas as pd
import random
import warnings
from nlpu import require_details, process_details
from training_ner import train_model
nlp = spacy.load("en_core_web_md")
updated_nlp = spacy.load('C:\\Users\\Adam\\Desktop\\Adam Biggs\\Student\\University\\4. Year Three (2021-2022)\\Artificial Intelligence\\CSW-2\\AI-Chatbot') # Change to relative path or your own path

if __name__ == "__main__":
     # model = train_model()
     data = require_details()
     process_details(data)
     # print("Group 26 Chatbot :D")
