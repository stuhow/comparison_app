import re

def airline_name(paragraph):
    pattern = re.compile(r"No [A-Z]+\d+\s+With ([A-Z\s]+)\s{3}")
    airlines_list = re.findall(pattern, paragraph)
    airlines = [airline.strip() for airline in airlines_list]
    return airlines

def departure_date():
    pass

def departure_airport():
    pass

def departure_city():
    pass

def departure_time():
    pass

def flight_number():
    pass

def class_of_travel():
    pass

def arival_airport():
    pass

def arrival_city():
    pass

def arrival_time():
    pass

def arrival_date():
    pass

def duration():
    pass

def airline_extraction(flight_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        if len(airline_name(paragraph)) > 0:
            flight_dict['Airline'].extend(airline_name(paragraph))

    return flight_dict
