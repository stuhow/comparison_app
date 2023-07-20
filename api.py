

flight_dict = {'Airline': ['AIR CANADA', 'AIR CANADA ROUGE', 'AIR CANADA EXPRESS', 'AIR CANADA'],
               'Arrival Airport': ['TORONTO', 'NEW ORLEANS,', 'TORONTO', 'LONDON (HEATHROW)'],
               'Arrival City': ['TORONTO', 'NEW ORLEANS,', 'TORONTO', 'LONDON'],
               'Arrival Date': ['2023-09-08', '2023-09-08', '2023-09-17', '2023-09-18'],
               'Arrival Time': ['11:15', '15:52', '21:40', '11:50'],
               'Arrival airport IATA code': ['YTOA', 'MSYA', 'YTOA', 'LHR'],
               'Class': ['ECONOMY', 'ECONOMY', 'ECONOMY', 'ECONOMY'],
               'Departure Airport': ['LONDON (HEATHROW)', 'TORONTO', 'NASHVILLE, TENNESSEE', 'TORONTO'],
               'Departure City': ['LONDON', 'TORONTO', 'NASHVILLE, TENNESSEE', 'TORONTO'],
               'Departure Date': ['2023-09-08', '2023-09-08', '2023-09-17', '2023-09-17'],
               'Departure Time': ['08:30', '14:00', '18:45', '23:40'],
               'Departure airport IATA code': ['LHR', 'YTOA', 'BNA', 'YTOA'],
               'Flight number': ['AC853', 'AC1711', 'AC8856', 'AC858']}

def add_multistop_flight_cost(flight_dict):
    '''a function to get flight costs'''

    # create legs value for all flights
    legs = []
    for i in range(len(flight_dict['Departure Date'])):
        legs.append({"origin":flight_dict["Departure airport IATA code"][i], "destination":flight_dict["Arrival airport IATA code"][i], "date":flight_dict["Departure Date"][i]})

    legs = str(legs).replace('\'','"').replace(" ","")
    print(legs)

add_multistop_flight_cost(flight_dict)

[{"origin":"LHR","destination":"YTOA","date":"2023-09-08"},\
    {"origin":"YTOA","destination":"MSYA","date":"2023-09-08"},\
    {"origin":"BNA","destination":"YTOA","date":"2023-09-17"},\
        {"origin":"YTOA","destination":"LHR","date":"2023-09-17"}]

[{"origin":"LHR","originEntityId":"95565050","destination":"JFK","destinationEntityId":"95565058","date":"2024-01-07"},\
    {"originEntityId":"95565058","destination":"LHR","destinationEntityId":"95565050","origin":"JFK","date":"2024-01-12"}]
