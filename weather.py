# import the module
import datetime
import python_weather
import asyncio

from ticket_details import Ticket

async def getweatherAt(ticket : Ticket):
    
       # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client()

    # fetch a weather forecast from a city
    weatherFrom = await client.find(f"{ticket.departure_station}, United Kingdom", )
    weatherTo = await client.find(f"{ticket.destination}, United Kingdom")

    a = weatherFrom.forecasts
    b = weatherTo.forecasts

    #If the day is not in scope of the weather infomation, nothing is printed.
    for forcast in weatherFrom.forecasts:
        if forcast.date.strftime("%d%m%Y") == ticket.date_of_departure:
            print(f"{ticket.departure_station}: On {forcast.day} the weather will be {forcast.sky_text} at {forcast.temperature} Degrees Celsius.")
            break

    for forcast in weatherTo.forecasts:
        if forcast.date.strftime("%d%m%Y") == ticket.date_of_departure:
            print(f"{ticket.destination}: On {forcast.day} the weather will be {forcast.sky_text} at {forcast.temperature} Degrees Celsius.")
            break

    await client.close()

if __name__ == "__main__":
    # ticket = Ticket('Namington','OXFORD', 'PENSARN','1645','26012022')

    # #if date is < 5 days beyond this one:
    # await getweatherAt(ticket)

    #Testing
    loop = asyncio.get_event_loop()
    
    ticket = Ticket('Namington','OXFORD', 'PENSARN','1645','26012022')

    #if date is < 5 days beyond this one:
    # loop.run_until_complete(getweatherAt(ticket))
    
    loop.run_until_complete(getweatherAt(ticket))
    
    # loop.run_until_complete(getweatherAt(ticket))