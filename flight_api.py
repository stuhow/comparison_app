

flight_dict = {'Airline': ['AIR CANADA', 'AIR CANADA ROUGE', 'AIR CANADA EXPRESS', 'AIR CANADA'],
               'Arrival Airport': ['TORONTO', 'NEW ORLEANS,', 'TORONTO', 'LONDON (HEATHROW)'],
               'Arrival City': ['TORONTO', 'NEW ORLEANS,', 'TORONTO', 'LONDON'],
               'Arrival Date': ['2023-09-08', '2023-09-08', '2023-09-17', '2023-09-18'],
               'Arrival Time': ['11:15', '15:52', '21:40', '11:50'],
               'Class': ['ECONOMY', 'ECONOMY', 'ECONOMY', 'ECONOMY'],
               'Departure Airport': ['LONDON (HEATHROW)', 'TORONTO', 'NASHVILLE, TENNESSEE', 'TORONTO'],
               'Departure City': ['LONDON', 'TORONTO', 'NASHVILLE, TENNESSEE', 'TORONTO'],
               'Departure Date': ['2023-09-08', '2023-09-08', '2023-09-17', '2023-09-17'],
               'Departure Time': ['08:30', '14:00', '18:45', '23:40'],
               'Flight number': ['AC853', 'AC1711', 'AC8856', 'AC858'],
               'Departure airport IATA code': ['LHR', 'YTOA', 'BNA', 'YTOA'],
               'Arrival airport IATA code': ['YTOA', 'MSYA', 'YTOA', 'LHR'],
               'Departure airport entity id': ['95565050', '27536640', '95673724', '27536640'],
               'Arrival airport entity id': ['27536640', '35234892', '27536640', '95565050']}

flight_dict = {'Airline': ['AIR CANADA', 'AIR CANADA ROUGE', 'AIR CANADA EXPRESS', 'AIR CANADA'],
               'Arrival Airport': ['TORONTO', 'NEW ORLEANS,', 'TORONTO', 'LONDON (HEATHROW)'],
               'Arrival City': ['TORONTO', 'NEW ORLEANS,', 'TORONTO', 'LONDON'],
               'Arrival Date': ['2023-09-08', '2023-09-08', '2023-09-17', '2023-09-18'],
               'Arrival Time': ['11:15', '15:52', '21:40', '11:50'],
               'Class': ['ECONOMY', 'ECONOMY', 'ECONOMY', 'ECONOMY'],
               'Departure Airport': ['LONDON (HEATHROW)', 'TORONTO', 'NASHVILLE, TENNESSEE', 'TORONTO'],
               'Departure City': ['LONDON', 'TORONTO', 'NASHVILLE, TENNESSEE', 'TORONTO'],
               'Departure Date': ['2023-09-08', '2023-09-08', '2023-09-17', '2023-09-17'],
               'Departure Time': ['08:30', '14:00', '18:45', '23:40'],
               'Flight number': ['AC853', 'AC1711', 'AC8856', 'AC858'],
               'Departure airport IATA code': ['LHR', 'YTOA', 'BNA', 'YTOA'],
               'Arrival airport IATA code': ['YTOA', 'MSYA', 'YTOA', 'LHR'],
               'Departure airport entity id': ['95565050', '27536640', '95673724', '27536640'],
               'Arrival airport entity id': ['27536640', '35234892', '27536640', '95565050']}

# [{"origin":"LHR","destination":"YTOA","date":"2023-09-08"},\
#     {"origin":"YTOA","destination":"MSYA","date":"2023-09-08"},\
#     {"origin":"BNA","destination":"YTOA","date":"2023-09-17"},\
#         {"origin":"YTOA","destination":"LHR","date":"2023-09-17"}]

# [{"origin":"LHR","originEntityId":"95565050","destination":"JFK","destinationEntityId":"95565058","date":"2024-01-07"},\
#     {"originEntityId":"95565058","destination":"LHR","destinationEntityId":"95565050","origin":"JFK","date":"2024-01-12"}]

import os
import requests
from thefuzz import process, fuzz

def get_flight_codes(city, airport):
    '''
    a function to get the airport code given a city and an airport given they may not be exact matches
    '''

    url = os.getenv("SEARCH_AIRPORT_ENDPOINT")

    querystring = {"query":city}

    headers = {
        "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
        "X-RapidAPI-Host": os.getenv("SKYSCANNER_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring).json()

    # get a list of airport names from in the city
    airports_list = [i['navigation']['localizedName'] for i in response['data']]

    # check which airport name is the closest match
    airport = process.extract(airport, airports_list, scorer=fuzz.ratio)[0][0]

    # position in list
    airport_position = airports_list.index(airport)

    # get iata code from list of airport dictionaries
    iata_code = response['data'][airport_position]['navigation']['skyId']

    entityid = response['data'][airport_position]['navigation']['entityId']

    return iata_code, entityid

def add_iata_codes(flight_dict):
    '''
    a function to add the iata codes for airports to the flight dictionary if they don't have one
    '''

    if "Departure airport IATA code" not in flight_dict.keys(): #check if iata code extracted from quote
        for i in range(len(flight_dict['Departure Date'])): #if not add new key to dict with code
            if "Departure airport IATA code" not in flight_dict.keys():
                flight_dict["Departure airport IATA code"] = [get_flight_codes(flight_dict['Departure City'][i], flight_dict['Departure Airport'][i])[0]]
            else:
                flight_dict["Departure airport IATA code"].append(get_flight_codes(flight_dict['Departure City'][i], flight_dict['Departure Airport'][i])[0])

    if "Arrival airport IATA code" not in flight_dict.keys():
        for i in range(len(flight_dict['Departure Date'])):
            if "Arrival airport IATA code" not in flight_dict.keys():
                flight_dict["Arrival airport IATA code"] = [get_flight_codes(flight_dict['Arrival City'][i], flight_dict['Arrival Airport'][i])[0]]
            else:
                flight_dict["Arrival airport IATA code"].append(get_flight_codes(flight_dict['Arrival City'][i], flight_dict['Arrival Airport'][i])[0])

    return flight_dict

def add_entity_codes(flight_dict):
    '''
    a function to add the iata codes for airports to the flight dictionary if they don't have one
    '''

    if "Departure airport entity id" not in flight_dict.keys(): #check if iata code extracted from quote
        for i in range(len(flight_dict['Departure Date'])): #if not add new key to dict with code
            if "Departure airport entity id" not in flight_dict.keys():
                flight_dict["Departure airport entity id"] = [get_flight_codes(flight_dict['Departure City'][i], flight_dict['Departure Airport'][i])[1]]
            else:
                flight_dict["Departure airport entity id"].append(get_flight_codes(flight_dict['Departure City'][i], flight_dict['Departure Airport'][i])[1])

    if "Arrival airport entity id" not in flight_dict.keys():
        for i in range(len(flight_dict['Departure Date'])):
            if "Arrival airport entity id" not in flight_dict.keys():
                flight_dict["Arrival airport entity id"] = [get_flight_codes(flight_dict['Arrival City'][i], flight_dict['Arrival Airport'][i])[1]]
            else:
                flight_dict["Arrival airport entity id"].append(get_flight_codes(flight_dict['Arrival City'][i], flight_dict['Arrival Airport'][i])[1])

    return flight_dict

# airline selector function needed?
def add_multistop_flight_cost(flight_dict):
    '''a function to get flight costs'''

    # create legs value for all flights
    legs = []
    for i in range(len(flight_dict['Departure Date'])):
        legs.append({"origin":flight_dict["Departure airport IATA code"][i],
                     "originEntityId":flight_dict["Departure airport entity id"][i],
                     "destination":flight_dict["Arrival airport IATA code"][i],
                     "destinationEntityId":flight_dict["Arrival airport entity id"][i],
                     "date":flight_dict["Departure Date"][i]})

    legs = str(legs).replace('\'','"').replace(" ","")

    url = os.getenv("SEARCH_FLIGHT_MULTISTOP_ENDPOINT")

    querystring = {"legs":legs,
                "waitTime":"10000",
                "adults":"1",
                "cabinClass":flight_dict['Class'][0].lower(),
                "currency":"GBP",
                "countryCode":"UK",
                "market":"en-GB"}

    headers = {
        "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
        "X-RapidAPI-Host": os.getenv("SKYSCANNER_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring).json()

    filtered_data = response['data']['itineraries']

    # is a function needed here to get the closest match to the airline names as they may not match?

    for i in range(len(flight_dict['Departure Date'])):

        # filtered_data = [item for item in filtered_data if item['legs'][i]['carriers'][0]['name'] == flight_dict['Airline'][i]]
        filtered_data = [item for item in filtered_data if item['legs'][i]['departure'][11:16] == flight_dict['Departure Time'][i]]

        # get airline name
        airline = flight_dict['Airline'][0].lower()

        # get a list of airline names
        airline_list = [i['legs'][0]['carriers']['marketing'][0]['name'].lower() for i in filtered_data]

        # check which airline name is the closest match
        airline = process.extract(airline, airline_list, scorer=fuzz.ratio)[0][0]

        filtered_data = [item for item in filtered_data if item['legs'][i]['carriers']['marketing'][0]['name'].lower() == airline]

    flight_dict['Flight cost per person'] = [filtered_data[0]['price']['raw']]

    while len(flight_dict['Flight cost per person']) < len(flight_dict['Departure Date']):
        flight_dict['Flight cost per person'].append(" - ")

    return flight_dict


print(add_multistop_flight_cost(flight_dict))
