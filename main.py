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
  #data = require_details()
  #process_details(data)
  # Create User Details class 