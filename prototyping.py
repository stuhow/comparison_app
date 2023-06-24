import requests
import os
from thefuzz import process
from thefuzz import fuzz


flight_dict = {'Departure Date': ['2023-09-21', '2023-09-28'],
               'Departure Airport': ['London Heathrow Airport', 'Logan International Airport'],
               'Departure City': ['London', 'Boston'],
               'Departure Time': ['14:40', '21:40'],
               'Flight number': ['BA0213', 'AA108'],
               'Airline': ['British Airways', 'British Airways'],
               'Class': ['Economy', 'Economy'],
               'Arival Airport': ['Logan International Airport', 'London Heathrow Airport'],
               'Arrival City': ['Boston', 'London'],
               'Arrival Time': ['17:00', '09:10'],
               'Arrival Date': ['2023-09-21', '2023-09-29'],
               'Duration': ['7 hours 20 minutes', '6 hours 30 minutes']}


def get_iata_code(city, airport):
    '''a function to get the airport code given a city and an airport given they may not be exact matches'''

    url = os.getenv("SEARCH_AIRPORT_ENDPOINT")

    querystring = {"query":city}

    headers = {
        "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
        "X-RapidAPI-Host": os.getenv("SKYSCANNER_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring)

    # get a list of airport names from in the city
    airports_list = [i['PlaceName'] for i in response.json()['data']]

    # check which airport name is the closest match
    airport = process.extract(airport, airports_list, scorer=fuzz.ratio)[0][0]

    # position in list
    airport_position = airports_list.index(airport)

    # get iata code from list of airport dictionaries
    iata_code = response.json()['data'][airport_position]['PlaceId']

    return iata_code
