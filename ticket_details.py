# This class is to contain all information regarding to a train ticket that the user inputs for a chatbot

class Ticket:
    def __init__(self, name, destination, departure_station, time_of_departure, date_of_departure):
        self.name = name
        self.destination = destination
        self.departure_station = departure_station
        self.time_of_departure = time_of_departure
        self.date_of_departure = date_of_departure

    def __str__(self):
        return f"{self.name}, {self.destination}, {self.departure_station}, {self.time_of_departure}, {self.date_of_departure}"




