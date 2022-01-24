import urllib.request
from bs4 import BeautifulSoup
from ticket_details import Ticket
from operator import attrgetter

# -------------------------
# File: web_crawler.py
# Classes: TicketFares, TicketFare
# Notes: This file is used to crawl and retrieve from the train times website NationalRail. 
# Author: Adam Biggs, ...
# -------------------------

class TicketFares():
  def __init__(self, ticketFares, url):
    self.ticketFares = ticketFares
    self.url = url

  def __getattribute__(self, item):
    return super(TicketFares, self).__getattribute__(item)

class TicketFare():
    def __init__(self, start, end, startTime, arrivalTime, length, cost):
      self.start = start
      self.end = end
      self.startTime = startTime
      self.arrivalTime = arrivalTime
      self.length = length
      self.cost = cost

    def __getattribute__(self, item):
      return super(TicketFare, self).__getattribute__(item)

def crawl(ticket : Ticket):
    # = 'cambridge' # in the form 'cambridge'
    # = 'norwich' # in the form 'norwich'
    # = '26012022' # in the form ddmmyyyy
    # = '1645' # in the form '1645' (hhmm)

    #testing
    start = ticket.departure_station  
    finish = ticket.destination       
    day = ticket.date_of_departure    
    time = ticket.time_of_departure   
    departing = 'dep'

    # https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/26012022/1645/dep#outwardJump

    url = f'https://ojp.nationalrail.co.uk/service/timesandfares/{start}/{finish}/{day}/{time}/{departing}#outwardJump'
    urlUsed, page_contents = get_webpage(url)

    htmlPage = BeautifulSoup(page_contents, 'html.parser')

    #This is an example of the html text I get BeautifulSoup to find. It holds all the infomation we need on two lines.
    # span class="fare-breakdown">
    # <input class="" type="hidden" value="SingleFare|1|Adult|Off-Peak Day Single||20.00||false|CDS|B5|LER|Greater Anglia|5|1|Travel is allowed via any permitted route.|ANY PERMITTED|FLEXIBLE|4"/>
    # </span>
    # <span class="journey-breakdown">
    # <input class="" type="hidden" value="Cambridge|CBG|16:46|Norwich|NRW|18:43|1|57|1|GREEN_TICK||"/>
    # </span>

    fareData = htmlPage.find_all("span",attrs={"class":"fare-breakdown"})
    journeyData = htmlPage.find_all("span",attrs={"class":"journey-breakdown"})

    ticketFares = []
    for iterator in range(5):
      fareDataLine = fareData[iterator].find("input")['value']
      journeyDataLine = journeyData[iterator].find("input")['value']

      fareDataLineArray = fareDataLine.split('|')

      _cost = fareDataLineArray[5]

      journeyDataLineArray = journeyDataLine.split('|')

      _start = f"{journeyDataLineArray[0]} [{journeyDataLineArray[1]}]" 
      _end = f"{journeyDataLineArray[3]} [{journeyDataLineArray[4]}]" 
      _startTime = f"{journeyDataLineArray[2]}" 
      _arrivalTime = f"{journeyDataLineArray[5]}"
      _length = f"{journeyDataLineArray[6]}h {journeyDataLineArray[7]}m"

      ticketFares.append(TicketFare(_start, _end, _startTime, _arrivalTime, _length, _cost))

    ticketFares.sort(key=attrgetter('cost'))

    return TicketFares(ticketFares, urlUsed)

def get_webpage(url):
  req = urllib.request.Request(url)
  try :
    f = urllib.request.urlopen(req) 

  except IOError as e :
    Exception("Error: Invalid URL")
  else:
     if (f.info().get_content_type() == "text/html"): #altered 03Oct15 DJS
         #print ("Sucess: " + url)
         try: 
           page_contents = f.read()
         except:
           Exception("Error: Unable to Read Page Contents")

         return f.geturl(), page_contents
     else:
         Exception("Error: Page is Not HTML")
  
if __name__ == "__main__":
	crawl(Ticket('','','','',''))