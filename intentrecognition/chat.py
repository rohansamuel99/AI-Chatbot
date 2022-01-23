#Implementation based off of 
#https://github.com/python-engineer/pytorch-chatbot
#Credit goes to original creators


import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

class IntentRecognition():
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        with open('C:/Users/rarihara/OneDrive - Agilent Technologies/Documents/Uni Stuff/AI CW/CW2/AI-Chatbot/intentrecognition/intents.json', 'r') as json_data:
            selfintents = json.load(json_data)

        FILE = "C:/Users/rarihara/OneDrive - Agilent Technologies/Documents/Uni Stuff/AI CW/CW2/AI-Chatbot/intentrecognition/data.pth"
        data = torch.load(FILE)

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def get_response(self, response):
        # sentence = "do you use credit cards?"
        
        sentence = tokenize(self.sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return- intent["tag"]
        else:
            print("I do not understand...")