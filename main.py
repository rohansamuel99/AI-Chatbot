import spacy
from spacy.training import Example
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
    ner = nlp.get_pipe('ner')
    
    snlp = spacy.load("en_core_web_md")
    df = pd.read_csv('stations.csv', header =0)
    df['ner_name'] = df['name'].astype(str).apply(lambda x: list(snlp(x).ents))
    pattern_to_replace = "{}"
    test_data = df['ner_name']
    print(len(test_data))
    label = "STATION"
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
      entities = []
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
      entities.append((start_index,end_index, 'STATION'))
    TRAIN_DATA.append((station_name_train_data, {"entities" : entities}))
    ner.add_label(label)
    optimizer = nlp.create_optimizer()

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
      for itn in range(20):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)
        print(losses)

    test_text = 'Liverpool Street london'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, " -- ", ent.text)






   

  #data = require_details()
  #process_details(data)
  # Create User Details class 
