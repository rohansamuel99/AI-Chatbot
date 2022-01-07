import spacy
import pandas as pd
import nltk
import re
import random
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from chatbot import require_details, process_details
nlp = spacy.load("en_core_web_md")

#python -m spacy download en_core_web_sm
if __name__ == "__main__":
    
    snlp = spacy.load("en_core_web_md")
    df = pd.read_csv('stations.csv', header =0)
    df['ner_name'] = df['name'].astype(str).apply(lambda x: list(snlp(x).ents))
    pattern_to_replace = "{}"
    test_data = df['ner_name']
    TRAIN_DATA = []
    # For every station, it has to have the format: 
    '''
    ("{} is a station in the UK", {"entities": [(0, 7, "STATION")]})
    first character index
    last character index
    name of entity tag/type
    '''
    train_sentence = "{} is a station in the UK"
    train_sentence2 = "I want to go to {} please"
    train_sentence3 = "I will be leaving from {}"
    list_train_sentences = [train_sentence,train_sentence2, train_sentence3]
    for every_station_name in test_data:
      station = str(every_station_name)
      # Randomly pick a sentence to for the station name, to create better training model
      picked_sentence = list_train_sentences[random.randint(0,len(list_train_sentences)-1)]
      # Formatting for station name in random sentence - simulating user input
      station_name_train_data = picked_sentence.format(station)
      # Index of first character in string
      start_index = station_name_train_data.index(station)

      # Index of last character in string
      end_index =station_name_train_data.rfind(station[-1]) 

      # Build spacy format









    '''
    while len(test_data) > 0:
      picked_station = test_data[random.randint(0,len(test_data) -1)]
      sentence = "{} is a train station in the UK"
      matches = re.findall(pattern_to_replace, sentence)
      for example in test_data:
        sentence = sentence.replace(example[0], picked_station,1)
        entities = []
        match_span = re.search(example,sentence).span()
        entities.append((match_span[0], match_span[1], 'STATION'))
      TRAIN_DATA.append((sentence,{"entities": entities}))

      '''

  #data = require_details()
  #process_details(data)
  # Create User Details class 
