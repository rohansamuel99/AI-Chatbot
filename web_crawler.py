# -------------------------
# File: web_crawler.py
# Classes: TicketFares, TicketFare
# Notes: This file is used to crawl and retrieve from the train times website NationalRail. 
# Author: Adam Biggs
# Date: 25/01/2022
# -------------------------

from tkinter import EXCEPTION
import urllib.request
from bs4 import BeautifulSoup
from ticket_details import Ticket
from operator import attrgetter

class TicketFares():
  # -------------------------
  # Class: TicketFares
  # Notes: This class is used to store the processed infomation about the ticket fares. As the url is the same
  #  for all ticket fares we store it here.
  # Author: Adam Biggs
  # Date: 25/01/2022
  # -------------------------
  def __init__(self, ticketFares, url):
    self.ticketFares = ticketFares
    self.url = url

  def __getattribute__(self, item):
    return super(TicketFares, self).__getattribute__(item)

class TicketFare():
    # -------------------------
    # Class: TicketFare
    # Notes: This class is used to store the processed infomation about an individual ticket fare. 
    #  for all ticket fares we store it here.
    # Author: Adam Biggs
    # Date: 25/01/2022
    # -------------------------
    def __init__(self, start, end, startTime, arrivalTime, length, cost):
      self.start = start
      self.end = end
      self.startTime = startTime
      self.arrivalTime = arrivalTime
      self.length = length
      self.cost = cost

    def __getattribute__(self, item):
      return super(TicketFare, self).__getattribute__(item)

#The crawl method forms the url using the supplied Ticket, then pulls all the HTML from the National Rail website.
# After this, it locates the two hidden span elements and extracts the data. Splits it into an array in each case and then
# forms a Ticket Fare from it. It collects 5 of them into a Ticket Fares object and sorts them on cost lowest to highest.
def crawl(ticket : Ticket):
    #Used to shorten the url below from a programmer view point.
    start = ticket.departure_station  
    finish = ticket.destination       
    day = ticket.date_of_departure    
    time = ticket.time_of_departure   
    departing = 'dep'

    #An example url which could be formed. Useful for testing.
    # https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/26012022/1645/dep#outwardJump

    #Form the url.
    url = f'https://ojp.nationalrail.co.uk/service/timesandfares/{start}/{finish}/{day}/{time}/{departing}#outwardJump'
    urlUsed, page_contents = get_webpage(url)

    #Use BeautifulSoup to parse the page contents into html.
    htmlPage = BeautifulSoup(page_contents, 'html.parser')

    #This is an example of the html text the program finds on National Rail. It holds all the infomation we need on two lines.
    # span class="fare-breakdown">
    # <input class="" type="hidden" value="SingleFare|1|Adult|Off-Peak Day Single||20.00||false|CDS|B5|LER|Greater Anglia|5|1|Travel is allowed via any permitted route.|ANY PERMITTED|FLEXIBLE|4"/>
    # </span>
    # <span class="journey-breakdown">
    # <input class="" type="hidden" value="Cambridge|CBG|16:46|Norwich|NRW|18:43|1|57|1|GREEN_TICK||"/>
    # </span>

    #Find the hidden spans.
    fareData = htmlPage.find_all("span",attrs={"class":"fare-breakdown"})
    journeyData = htmlPage.find_all("span",attrs={"class":"journey-breakdown"})

    if len(fareData) == 0 or len(journeyData) == 0:
      return Exception("ERROR: No Data Found. Make sure the date and time was in the future.")

    ticketFares = []
    #For every index...
    for iterator in range(5):
      #...find the value attribute...
      fareDataLine = fareData[iterator].find("input")['value']
      journeyDataLine = journeyData[iterator].find("input")['value']

      #...and split it on '|'...
      fareDataLineArray = fareDataLine.split('|')

      _cost = fareDataLineArray[5]

      journeyDataLineArray = journeyDataLine.split('|')

      _start = f"{journeyDataLineArray[0]} [{journeyDataLineArray[1]}]" 
      _end = f"{journeyDataLineArray[3]} [{journeyDataLineArray[4]}]" 
      _startTime = f"{journeyDataLineArray[2]}" 
      _arrivalTime = f"{journeyDataLineArray[5]}"
      _length = f"{journeyDataLineArray[6]}h {journeyDataLineArray[7]}m"

      #...and append the data to a ticketFares array.
      ticketFares.append(TicketFare(_start, _end, _startTime, _arrivalTime, _length, _cost))

    #Sort the array on cost.
    ticketFares.sort(key=attrgetter('cost'))

    return TicketFares(ticketFares, urlUsed)

#Procedure attempts to find and read the contents of the website. It provides error messages if it is unsuccessful.
def get_webpage(url):
  req = urllib.request.Request(url)
  try :
    f = urllib.request.urlopen(req) 

  except IOError as e :
    Exception("Error: Invalid URL")
  else:
     if (f.info().get_content_type() == "text/html"): 
         try: 
           page_contents = f.read()
         except:
           Exception("Error: Unable to Read Page Contents")

         return f.geturl(), page_contents
     else:
         Exception("Error: Page is Not HTML")
  
#For Testing.
if __name__ == "__main__":
	crawl(Ticket('','','','',''))