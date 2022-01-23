from intentrecognition.chat import *
from intentrecognition.nltk_utils import stem
from spell_checker import SpellChecker
import re
import spacy
from database_handler import DatabaseHandler
from datetime import *
import nltk
from nltk.stem import PorterStemmer
# from pathlib import Path
# from spacy.pipeline import EntityRuler
from dateutil.relativedelta import *


#get_user_response
#return_chatbot_answer


#Used to select the method of reasoning
def reasoning(message, context):
    message = message.lower()
    #stemming
    if context == "basic":
        answer = stemmer(message)
    
    #Access train stations in the message
    if context == "loc":
        answer= get_locations(message)

    #Get a date from a users message
    if context == "date":
        answer= get_date(message)

    #Get a time from a users message
    if context == "time":
        answer= get_time(message)
        return answer

    #Get a delay time from a users message
    if context == "delay":
        answer =get_delay(message)
        
    if context == "booking":
        answer = get_booking_info(message)
        return answer

    if context == "initial":
        model = IntentClassification()
        answer = model.get_response(message)
        return answer

    if context == "yesno":
        answer = get_yes_no(message)
        return answer

    #If an answer was found return it
    if answer!=None:
        return answer
    else:
        #If the reasoning engine could not understand the users message, check possible spelling mistakes
        spellChecker = SpellChecker()
        words = message.split(" ")
        try:
            #Find all spelling mistakes in the message and replace them
            for i in range(len(words)):
                wordspellcheck = re.sub("[/\d-]","",words[i])
                correct = spellChecker.make_correction(wordspellcheck)
                if wordspellcheck != correct and wordspellcheck!="":
                    returnChatbotAnswer("Did you mean "+ correct+"?")
                    while True:
                        query = getUserResponse().lower()
                        answer = get_yes_no(query)
                        if "yes" == query:
                            words[i] = correct
                            break
                        elif "no" == query:
                            break
                        else:
                            returnChatbotAnswer("Sorry I could not understand your response, please answer yes or no")
        except:return None
        message = " ".join(words)
        #Attempt to find an answer again with the spelling mistakes fixed
        if context == "basic":
            answer= stemmer(message)
        if context == "loc":
            answer= get_locations(message)
        if context == "date":
            answer= get_date(message)
        if context == "time":
            answer= get_time(message)
        if context == "delay":
            answer =get_delay(message)
        if answer!=None:
            return answer
        
    #open flaskserver/acquistion.txt and append
    #If no answer could be found, return None
    return None

#########station_ner and patterns.json?
# def get_booking_info(message):
#     message=re.sub("['\(\)]","",message)
#     ner_path = Path("./station_ner")
#     nlp = spacy.load(ner_path)
#     ruler = EntityRuler(nlp,overwrite_ents=True).from_disk("./station_ner/patterns.jsonl")
#     nlp.add_pipe(ruler)
#     #Apply NER to the users message
#     doc = nlp(message)
#     departure=None
#     arrival=None
#     for ent in doc.ents:
#         if ent.label_ == "LOC":
#             station = check_station_exists(ent.text)
#             if station != None:
#                 if str(doc[ent.start-1])=="to":
#                     arrival=station
#                 elif str(doc[ent.start-1])=="from":
#                     departure=station
#                 else:
#                     pass
#     date=get_date(message)
#     time = get_time(message)
#     print(departure,arrival,date,time)
#     return {"departure":departure,"arrival":arrival,"date":date,"time":time}

#Implement basic spacy named entity recognition
def basic_spacy_ner(message):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(message)
    return doc

def check_station_exists(station_name):
    database = DatabaseHandler()
    test_station=station_name
    answer = database.checkStation(test_station)
    if answer==False:
        return None
    else:
        #If only one station matched the location, return it
        if len(answer)==1:
            answer = answer[0][1]
            database.close()
            return answer
        else:
            #If more than one station matched the location found
            for station in  answer:
                #Check if any station name is an exact match with the found location
                if station[1]==test_station:
                    answer = station[1]
                    database.close()
                    return answer
    database.close()

############def get_locations

#Basic nltk stemmer implementation
def stemmer(message):
    stemmer = PorterStemmer()
    message_token = nltk.word_tokenize(message)
    stemmed_message=[]
    for count in range(len(message_token)):
        stemmed_message.append(stemmer.stem(message_token[count]))
    return stemmed_message

def get_date(message):
    final=""
    tokens = nltk.word_tokenize(message)
    for token in tokens:
        try:
            mat=re.match('(\d{2})[/.-](\d{2})[/.-](\d{4})$', token)
            if mat is not None:
                datetime(*(map(int, mat.groups()[-1::-1])))
                final=convert_date_to_format(token)
                break
        except ValueError:
            pass
    if final == "":
        test=basic_spacy_ner(message)
        for ent in test.ents:
            if ent.label_=="DATE":
                date=ent.text
                final = convert_date_to_format(date)
                break
    if final!="":
        return final
    return None

def convert_date_to_format(base_date):
    final=""
    if re.match("\d{2}[/]\d{2}[/]\d{4}",base_date)!=None:
        test=base_date.split("/")
        final = str(test[0])+str(test[1])+str(test[2])
    elif re.match("\d{2}[-]\d{2}[-]\d{4}",base_date)!=None:
        test=base_date.split("-")
        final = str(test[0])+str(test[1])+str(test[2])
    else:
        if base_date=="tomorrow" or base_date=="today":
            final = datetime.today()
            if base_date=="tomorrow":
                final=final+relativedelta(days=+1)
            final=final.strftime('%Y-%m-%d')
            final=final.split("-")
            final.reverse()
            final = str(final[0])+str(final[1])+str(final[2])
        else:
            date = re.search("\d{1,2}((st)|(nd)|(rd)|(th))",base_date)
            if date is not None:
                intdate=base_date[date.span()[0]:date.span()[1]-2]
                year = re.search("\d{4}",base_date)
                if year is not None:
                    intyear=base_date[year.span()[0]:year.span()[1]]
                    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
                    base_date=base_date.split(" ")
                    month=""
                    for word in base_date:
                        word = word.lower()
                        if word in months:
                            month = word
                            break
                    if month!= "":
                        try:
                            final=datetime.strptime(str(intdate)+"/"+str(month)+"/"+str(intyear), '%d/%B/%Y').strftime('%d%m%Y')
                        except:
                            pass
    if final!="":
        datetimeformat = datetime.strptime(final,"%d%m%Y")
        if datetimeformat.date()<datetime.today().date():
            return "invalid"
        return final
    else:
        return None
    
def get_time(message):
    potential_time = re.findall("(\d{1,2}(:\d{2})?\s*(am|pm)?)",message)
    if len(potential_time) > 0:
        time = potential_time[0][0]
        if "am" in time:
            if ":" in time:
                timesplit = time.split(":")
                hour = timesplit[0]
                if int(hour)==12:
                    hour="00"
                if len(hour)<2:
                    hour="0"+hour
                minute=timesplit[1][:2]

                if 0<=int(hour)<=24 and 0<=int(minute)<=59:
                    return str(hour)+":"+str(minute)
            else:
                hour = re.findall("\d{1,2}",time)
                hour=hour[0]
                if int(hour)==12:
                    hour="00"
                if len(hour)<2:
                    hour="0"+hour
                if 0<=int(hour)<=24:
                    return hour+":00"
        elif "pm" in time:
            if ":" in time:
                timesplit = time.split(":")
                hour = timesplit[0]
                if int(hour)<12:
                    hour = str(int(hour)+12)
                minute=timesplit[1][:2]
                if 0<=int(hour)<=24 and 0<=int(minute)<=59:
                    return str(hour)+":"+str(minute)
            else:
                hour = re.findall("\d{1,2}",time)
                hour=hour[0]
                if int(hour)<12:
                    hour = str(int(hour)+12)
                if 0<=int(hour)<=24:
                    return hour+":00"
        else:
            if ":" in time:
                timesplit = time.split(":")
                hour = timesplit[0]
                minute=timesplit[1][:2]
                if 0<=int(hour)<=24 and 0<=int(minute)<=59:
                    return str(hour)+":"+str(minute)
            else:
                hour = re.findall("\d{1,2}",time)
                hour=hour[0]
                if 0<=int(hour)<=24:
                    return hour+":00"
    return None

def get_delay(message):
    message=basic_spacy_ner(message)
    for ent in message.ents:
        if ent.label_=="TIME":
            items = (ent.text).split(" ")
            if items[1].lower() == "minutes" or items[1].lower() == "mins":
                return items[0]
    return None

def get_yes_no(message):
    yeswords = ["yes","y","yep","yeah"]
    nowords = ["no","nope","n","nah"]
    if any(word in yeswords for word in message):
        return "yes"
    elif any(word in nowords for word in message):
        return "no"
    else:
        return None

if __name__ == "__main__":
##    text = ["I am travelling on 20/02/2021",
##            "today",
##            "My journey is tomorrow",
##            "I want to leave on the 20th of february 2021",
##            "March 10th 2021",
##            "I dont know",
##            "I want to travel yesterday",
##            "01/01/2021",
##            "30/02/2021",
##            "99/99/9999"]
##    for i in text:
##        print(get_date(i))
    text = "I want a train from norwich to diss at 3pm on january 13th 2022"
    print(text)
    print(reasoning(text,"booking"))