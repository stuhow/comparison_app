from companies.abercrombie import abercrombie_dictionaries
from companies.trailfinders import trailfinders_dictionaries
import requests
import os
from thefuzz import process
from thefuzz import fuzz
from PyPDF2 import PdfFileReader
import pdftotext


def select_company(text):
    if 'abercrombie' in text:
        return 'Abercrombie & Kent'
    if 'trailfinders' in text:
        return 'Trailfinders'

def get_data(text, company):
    if company == "Abercrombie & Kent":
        return abercrombie_dictionaries(text)
    if company == "Trailfinders":
        return trailfinders_dictionaries(text)





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
            if flight_dict['Arival Airport'][i] in flight_dict['Departure Airport']: # check if we already got the iata code in departure airports
                airport_index = flight_dict['Departure Airport'].index(flight_dict['Arival Airport'][i])
                if "Arrival airport IATA code" not in flight_dict.keys():
                    flight_dict["Arrival airport IATA code"] = [flight_dict['Departure airport IATA code'][airport_index]]
                else:
                    flight_dict["Arrival airport IATA code"].append(flight_dict['Departure airport IATA code'][airport_index])
            else:
                if "Arrival airport IATA code" not in flight_dict.keys(): # if arival airport not in departures get the airport code
                    flight_dict["Arrival airport IATA code"] = [get_iata_code(flight_dict['Arrival City'][i], flight_dict['Departure Airport'][i])]
                else:
                    flight_dict["Arrival airport IATA code"].append(get_iata_code(flight_dict['Arrival City'][i], flight_dict['Departure Airport'][i]))

    return flight_dict

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
        filtered_data = [item for item in filtered_data if item['legs'][i]['carriers'][0]['name'] == flight_dict['Airline'][i]]
        filtered_data = [item for item in filtered_data if item['legs'][i]['departure'][11:16] == flight_dict['Departure Time'][i]]

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

def add_hotel_details(hotel_dict):
    for i in range(len(hotel_dict['Check-in Date'])):

        full_hotel_name = hotel_dict['Hotel name'][i] + ", " + hotel_dict['Location'][i]

        url = os.getenv("HOTEL_LOCATION_ENDPOINT")

        querystring = {"name":full_hotel_name[:50:],
                        "locale":"en-gb"}

        headers = {
            "X-RapidAPI-Key": os.getenv("BOOKING_API_KEY"),
            "X-RapidAPI-Host": os.getenv("BOOKING_API_HOST")
        }

        response = requests.get(url, headers=headers, params=querystring)

        response= response.json()

        hotel_id = response[0]['dest_id']


        url = os.getenv("HOTEL_SEARCH_ENDPOINT")

        querystring = {"order_by":"popularity",
                        "adults_number":"2",
                        "checkin_date":hotel_dict['Check-in Date'][i],
                        "filter_by_currency":"GBP",
                        "dest_id":hotel_id,
                        "locale":"en-gb",
                        "checkout_date":hotel_dict['Check-out Date'][i],
                        "units":"metric",
                        "room_number":"1",
                        "dest_type":"hotel"}

        headers = {
            "X-RapidAPI-Key": os.getenv("BOOKING_API_KEY"),
            "X-RapidAPI-Host": os.getenv("BOOKING_API_HOST")
        }

        response = requests.get(url, headers=headers, params=querystring).json()

        total_price = None
        if response['results'][0]['priceBreakdown'] == None:
            total_price = 'Sold out on booking.com'
        else:
            grossPrice = response['results'][0]['priceBreakdown']['grossPrice']['value']

            if 'excludedPrice' in response['results'][0]['priceBreakdown'].keys():
                excludedPrice = response['results'][0]['priceBreakdown']['excludedPrice']['value']
                total_price = round(excludedPrice + grossPrice)
            else:
                total_price = round(grossPrice)

        review_score = response['results'][0]['reviewScore']

        if 'Starting price on Booking.com' not in hotel_dict.keys():
            hotel_dict['Starting price on Booking.com'] = [total_price]
        else:
            hotel_dict['Starting price on Booking.com'].append(total_price)

        if 'Review score on Booking.com' not in hotel_dict.keys():
            hotel_dict['Review score on Booking.com'] = [review_score]
        else:
            hotel_dict['Review score on Booking.com'].append(review_score)

    return hotel_dict
