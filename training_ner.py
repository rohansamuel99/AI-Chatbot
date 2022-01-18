import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import pandas as pd
import random
import warnings
nlp = spacy.load("en_core_web_md")

def train_model():
    ner = nlp.get_pipe('ner')
    # Reading from file and extracting value into list
    df = pd.read_csv('stations.csv', usecols=[0])
    station_list = df["name"].to_csv(header=None).split(',')
    station_list = [col.replace('\r\n', '').replace('(', '').strip().lower() for col in station_list]
    TRAIN_DATA = []
    '''
    For every station, it has to have the format:
    ("{} is a station in the UK", {"entities": [(0, 7, "STATION")]})
    first character index
    last character index
    name of entity tag/type
    '''
    train_sentence = "{} is a station in the UK"
    used_station_list = []
    for every_station_name in station_list:
        try:
            entities = []
            station = str(every_station_name)
            station_in_sentence = train_sentence.format(station)
            start_index = station_in_sentence.index(station)
            end_index = station_in_sentence.index(station) + len(station)
            # Build spacy format
            entities.append((start_index, end_index, 'STATION'))
            if station_in_sentence not in TRAIN_DATA:
                TRAIN_DATA.append((station_in_sentence, {"entities": entities}))
                used_station_list.append(every_station_name)
                station_list.remove(every_station_name)
        except IndexError as i_error:
            print("empty station name", i_error)

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Disable pipeline components you don't need to change
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    with nlp.disable_pipes(*unaffected_pipes):  # only train NER
        for itn in range(20):
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                text, annotations = zip(*batch)
                example = []
                # Update the model with iterating each text
                for i in range(len(text)):
                    doc = nlp.make_doc(text[i])
                    example.append(Example.from_dict(doc, annotations[i]))

                # Update the model
                nlp.update(example, drop=0.5, losses=losses)
                print("Losses", losses)

    # -----------------------------------------------------------------------
    # Saving & Loading the new NER Model

        output_dir = Path('C:/Users/Samuel/Documents/AI-Chatbot') # Change to relative path or your own path
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
        # Load the saved model and predict
        print("Loading from", output_dir)
        nlp_updated = spacy.load(output_dir)
        return nlp_updated
    '''
    doc = nlp_updated("Manchester is a station in the uk")
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    doc = nlp("Liverpool Street is a station in the uk")
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    '''


