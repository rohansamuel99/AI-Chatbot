#https://ojp.nationalrail.co.uk/service/timesandfares/NRW/Oxford_Circus/tomorrow/1630/dep

from datetime import datetime
import sys
import os.path
from urllib.parse import urlparse
import webbrowser


# Global constants for special conditions when fetching web pages
invalid_URL =       "[-- invalid url --]"
error_reading_URL = "[-- error reading URL --]"
password_URL =      "[-- password url --]"
protected_URL =     "[-- protected url --]"
not_text_URL =      "[-- not text/html url --]"
timeout_URL =       "[-- timed out URL --]"
  
URL_errors = set([invalid_URL, error_reading_URL,  password_URL, \
    protected_URL, not_text_URL, timeout_URL ])

#########################
#<<<<< get_webpage module 
#########################

from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urlunsplit

from bs4 import BeautifulSoup
import re

Permissions = {}

class Ticket():
  def __init__(self, time, startStation, endStation, timeLength, cost):
    self.time = time
    self.startStation = startStation
    self.endStation = endStation
    self.timeLength = timeLength
    self.cost = cost
    


def main():
  start = 'Aberdeen Rail Station'
  destination = 'Abergavenny Rail Station'
  day = 'tomorrow'
  time = '1630'
  departing = 'dep'

  getRoutes(start, destination, day, time, departing)

def getRoutes(start, destination, day, time, departing):

    # https://ojp.nationalrail.co.uk/service/timesandfares/NRW/Oxford_Circus/tomorrow/1630/dep#outwardJump


    # google maps might do it:
    # google maps train 16/01/2022 10am norwich to standsted
    # https://www.google.com/search?q=google+maps+train+16%2F01%2F2022+10am+norwich+to+standsted&client=firefox-b-d
    # google maps train 16/01/2022 10am ASCOTT-UNDER-WYCHWOOD to ARUNDEL
    #
    # maybe if it searched 'google maps train 16/01/2022 10am ASCOTT-UNDER-WYCHWOOD to ARUNDEL'
    # then after crawled the website for buy ticket to find the first '£' then use that for the money

    #problems
    # - If no route exists (if is a stupid time)
    # - If multiple tickets are required then it gives a stupid popup - should still work
    #    (https://ojp.nationalrail.co.uk/service/timesandfares/AXP/AGV/210122/0930/dep)


    url = f'https://ojp.nationalrail.co.uk/service/timesandfares/{start}/{destination}/{day}/{time}/{departing}#outwardJump'
    timestamp, urlUsed, page_contents = get_webpage(url)

    textWithoutHtml = BeautifulSoup(page_contents, 'html.parser')

    plaintext = re.sub("Â\xa0", ' ', textWithoutHtml.text)
    plaintext = re.sub("\n", ' ', plaintext)
    plaintext = re.sub("\t", ' ', plaintext)
    plaintext = re.sub(" + ", ',', plaintext)

    

    #also need remove \t \n and Â\xa0


    #use fancy text stuff to remove empty characters!!!!!!!!!!!!

    ticketPlaintextArray = plaintext.split('Departs at')
    ticketPlaintextArray.pop(0)

    tickets = []
    for ticketData in ticketPlaintextArray:
      ticketDataArray = ticketData.split(',')
      tickets.append(Ticket(ticketDataArray[0],
       ticketDataArray[1] + ticketDataArray[2],
       ticketDataArray[10], 
       ticketDataArray[3] + ticketDataArray[4], 
       ticketDataArray[18]))

    # https://ojp.nationalrail.co.uk/service/purchaseticket/handoff?url=https://ojp.nationalrail.co.uk/service/timesandfares/NRW/Oxford_Circus/tomorrow/1630/dep#outwardJump
    # https://ojp.nationalrail.co.uk/service/purchaseticket/handoff?url=https://ojp.nationalrail.co.uk/service/timesandfares/NRW/Oxford_Circus/tomorrow/1630/dep#outwardJump


    # launch the website with the tickets on it.
    webbrowser.open(url)

    a = 0

# def domain_name(url):
#     return urlparse(url)[1]

# def can_read(url):

#   domain = domain_name(url)
#   if domain not in Permissions :
#          rp = RobotFileParser()
#          rp.set_url(urljoin('http://' + domain, 'robots.txt'))
#          try :
#             rp.read()
#          except:
#             return False
         
#          Permissions[domain] = rp

#   res = False
#   try:
#     res  = Permissions[domain].can_fetch("*", url)
#   except:
#     return False

#   return res

def get_webpage(url):

  timestamp = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") 
  #print "get_webpage(" + url + ")"
#   if not can_read(url)  :
#       return timestamp, url, protected_URL

  #  try to open url, if unsuccessful, return default info and exit
  #

  req = urllib.request.Request(url)
  try :
    #print "Opening: " + url
    f = urllib.request.urlopen(req) 
    #print "Opened: " + url
  #
  # changed IOError to "anything" , since urlopen sometimes throws
  # httplib.BadStatusLine() exception, which apparently is not
  # covered under IOError.
  #
  except IOError as e :
     #print "IOError, e: "
     if hasattr(e, 'code'):
        if e.code == 401 :
          #print "Error 401: " 
          return timestamp, url, password_URL
        else :
          return timestamp, url, invalid_URL

     else:
          #print "No e-code"
          return timestamp, url, invalid_URL
  except: 
        return timestamp, url,  invalid_URL
  else:
   
     if (f.info().get_content_type() == "text/html"): #altered 03Oct15 DJS
         #print ("Sucess: " + url)
         try: 
           page_contents = f.read()
         except:
           page_contents = error_reading_URL

         return timestamp, f.geturl(), page_contents
     elif (f.info().get_content_type() == "application/pdf"): #added 22Oct15 DJS
         print ('get_webpage: Found a PDF', url)
         return timestamp, f.geturl(), not_text_URL
     else:
         #print ("not text/html: " + url)
         return timestamp, f.geturl(), not_text_URL
       


if __name__ == "__main__":
	main()