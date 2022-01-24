# Implementation based off of design from
# http://norvig.com/spell-correct.html
# Credit goes to Peter Norvig for original creation

import re
from collections import Counter
import csv
import json

class SpellChecker():

    def __init__(self):
        with open('C:/Users/rarihara/OneDrive - Agilent Technologies/Documents/Uni Stuff/AI CW/CW2/AI-Chatbot/words.json', 'r') as file:
            self.words_list = json.load(file)
        
    def probability_of_words(self, word):
        N = sum(self.words_list.values())
        return self.words_list[word] / N

    def correction(self, word):
        return max(self.candidate_words(word), key = self.probability_of_words)
    
    def candidate_words(self, word):
        return (self.known_words([word]) or self.known_words(self.edit_word(word)) or self.known_words(self.two_edit_check(word)) or [word])

    def known_words(self, words):
        return set(w for w in words if w in self.words_list)
    
    def edit_word(self, word):
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
    
    def two_edit_check(self, word):
        return (e2 for e1 in self.edit_word(word) for e2 in self.edit_word(e1))

    def buildWordList(self):
        words={}
        with open("stations.csv",newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',',)
            skipfirst=True
            for row in reader:
                if skipfirst:
                    skipfirst=False
                    pass
                else:
                    station = (row[0]).lower()
                    station=re.sub("['\(\)]","",station)
                    stationname = station.split(" ")
                    for word in stationname:
                        if len(word)>1:
                            try:
                                words[word]+=1
                            except:
                                words[word]=1
        months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
        for month in months:
            try:
                words[month]+=1
            except:
                words[month]=1
        otherwords=["book","minutes","hours","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        for word in otherwords:
            try:
                words[word]+=1
            except:
                words[word]=1
        
        with open("C:/Users/rarihara/OneDrive - Agilent Technologies/Documents/Uni Stuff/AI CW/CW2/AI-Chatbot/words.json","w") as file:
            json.dump(words,file)

if __name__ == "__main__":
    spell_checker = SpellChecker()
    corrected_word = spell_checker.correction("nveber")
    print(corrected_word)

    spell_checker = SpellChecker()
    corrected_word = spell_checker.correction("wenesdy")
    print(corrected_word)