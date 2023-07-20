import os
import requests
from thefuzz import process, fuzz

def get_iata_code(city, airport):
    '''
    a function to get the airport code given a city and an airport given they may not be exact matches
    '''

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

def add_iata_code(flight_dict):
    '''
    a function to add the iata codes for airports to the flight dictionary if they don't have one
    '''

    if "Departure airport IATA code" not in flight_dict.keys(): #check if iata code extracted from quote
        for i in range(len(flight_dict['Departure Date'])): #if not add new key to dict with code
            if "Departure airport IATA code" not in flight_dict.keys():
                flight_dict["Departure airport IATA code"] = [get_iata_code(flight_dict['Departure City'][i], flight_dict['Departure Airport'][i])]
            else:
                flight_dict["Departure airport IATA code"].append(get_iata_code(flight_dict['Departure City'][i], flight_dict['Departure Airport'][i]))

    if "Arrival airport IATA code" not in flight_dict.keys():
        for i in range(len(flight_dict['Departure Date'])):
            if "Arrival airport IATA code" not in flight_dict.keys():
                flight_dict["Arrival airport IATA code"] = [get_iata_code(flight_dict['Arrival City'][i], flight_dict['Arrival Airport'][i])]
            else:
                flight_dict["Arrival airport IATA code"].append(get_iata_code(flight_dict['Arrival City'][i], flight_dict['Arrival Airport'][i]))
    print(flight_dict)
    return flight_dict

# airline selector function needed?
def add_multistop_flight_cost(flight_dict):
    '''a function to get flight costs'''

    # create legs value for all flights
    legs = []
    for i in range(len(flight_dict['Departure Date'])):
        legs.append({"origin":flight_dict["Departure airport IATA code"][i], "destination":flight_dict["Arrival airport IATA code"][i], "date":flight_dict["Departure Date"][i]})

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

    filtered_data = response['data']

    # is a function needed here to get the closest match to the airline names as they may not match?

    for i in range(len(flight_dict['Departure Date'])):

        # filtered_data = [item for item in filtered_data if item['legs'][i]['carriers'][0]['name'] == flight_dict['Airline'][i]]
        filtered_data = [item for item in filtered_data if item['legs'][i]['departure'][11:16] == flight_dict['Departure Time'][i]]

        # get airline name
        airport = flight_dict['Airline'][0].lower()

        # get a list of airline names
        airports_list = [i['legs'][0]['carriers'][0]['name'].lower() for i in filtered_data]

        # check which airport name is the closest match
        airport = process.extract(airport, airports_list, scorer=fuzz.ratio)[0][0]

        filtered_data = [item for item in filtered_data if item['legs'][i]['carriers'][0]['name'].lower() == airport]

    flight_dict['Flight cost per person'] = [filtered_data[0]['price']['amount']]

    while len(flight_dict['Flight cost per person']) < len(flight_dict['Departure Date']):
        flight_dict['Flight cost per person'].append(" - ")

    return flight_dict

def add_flight_cost(flight_dict):

    url = os.getenv("SEARCH_FLIGHT_ENDPOINT")

    querystring = {"origin":flight_dict['Departure airport IATA code'][0],
                "destination":flight_dict['Arrival airport IATA code'][0],
                "date":flight_dict['Departure Date'][0],
                "returnDate":flight_dict['Departure Date'][1],
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

    filtered_data = response['data']

    # is a function needed here to get the closest match to the airline names as they may not match?

    for i in range(len(flight_dict['Departure Date'])):
        filtered_data = [item for item in filtered_data if item['legs'][i]['carriers'][0]['name'] == flight_dict['Airline'][i]]
        filtered_data = [item for item in filtered_data if item['legs'][i]['departure'][11:16] == flight_dict['Departure Time'][i]]

    flight_dict['Flight cost per person'] = [filtered_data[0]['price']['amount']]

    while len(flight_dict['Flight cost per person']) < len(flight_dict['Departure Date']):
        flight_dict['Flight cost per person'].append(" - ")


    return flight_dict
