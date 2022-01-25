# -------------------------
# File: weather.py
# Notes: This file is used to collect weather infomation on a given Ticket. 
#  It is used to provide the user with weather infomation for the start and end of their journey.
# Author: Adam Biggs
# Date: 25/01/2022
# -------------------------

#Import the python_weather module.
import python_weather
import asyncio

from ticket_details import Ticket

async def getweatherAt(ticket : Ticket):
    
    #Declare the client, the format of which defaults to the metric system.
    client = python_weather.Client()

    #Fetch the weather from the two locations, specifying that they are within the UK.
    weatherFrom = await client.find(f"{ticket.departure_station}, United Kingdom", )
    weatherTo = await client.find(f"{ticket.destination}, United Kingdom")

    #For every day in the 5 day forcast, the program prints infomation about they one that is the ticket's date. 
    # If the day is not in scope of the weather infomation, nothing is printed.
    for forcast in weatherFrom.forecasts:
        if forcast.date.strftime("%d%m%Y") == ticket.date_of_departure:
            print(f"{ticket.departure_station}: On {forcast.day} the weather will be {forcast.sky_text} at {forcast.temperature} Degrees Celsius.")
            break

    for forcast in weatherTo.forecasts:
        if forcast.date.strftime("%d%m%Y") == ticket.date_of_departure:
            print(f"{ticket.destination}: On {forcast.day} the weather will be {forcast.sky_text} at {forcast.temperature} Degrees Celsius.")
            break
    
    #Close the connection to the API.
    await client.close()

#Testing.
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ticket = Ticket('Namington','OXFORD', 'PENSARN','1645','26012022')
    loop.run_until_complete(getweatherAt(ticket))