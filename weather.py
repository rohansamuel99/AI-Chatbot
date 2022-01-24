# import the module
import datetime
import python_weather
import asyncio

from ticket_details import Ticket

async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("Washington DC")

    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    # get the weather forecast for a few days
    for forecast in weather.forecasts:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)

    # close the wrapper once done
    await client.close()

async def getweatherAt(ticket : Ticket):
       # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client()

    # fetch a weather forecast from a city
    weatherFrom = await client.find(f"{ticket.departure_station}, United Kingdom", )
    weatherTo = await client.find(f"{ticket.destination}, United Kingdom")

    

    a = weatherFrom.forecasts
    b = weatherTo.forecasts



    for forcast in weatherFrom.forecasts:
        if forcast.date.strftime("%d%m%Y") == ticket.date_of_departure:
            print(f"On {forcast.day} the weather will be {forcast.sky_text} at {forcast.temperature} Degrees Celsius.")
            break

    for forcast in weatherFrom.forecasts:
        if forcast.date.strftime("%d%m%Y") == ticket.date_of_departure:
            print(f"On {forcast.day} the weather will be {forcast.sky_text} at {forcast.temperature} Degrees Celsius.")
            break


    b = 0

    # class Ticket:
    # def __init__(self, name, destination, departure_station, time_of_departure, date_of_departure):
    #     self.name = name
    #     self.destination = destination
    #     self.departure_station = departure_station
    #     self.time_of_departure = time_of_departure
    #     self.date_of_departure = date_of_departure

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())  

    ticket = Ticket('Namington','OXFORD', 'PENSARN','1645','26012022')

    #if date is < 5 days beyond this one:
    loop.run_until_complete(getweatherAt(ticket))