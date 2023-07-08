import re
from companies.helper.trailfinders_helper_functions import date_conversion_function

# from helper.trailfinders_helper_functions import date_conversion_function

def airline_name(paragraph):
    pattern = re.compile(r"No [A-Z]+\d+\s+With ([A-Z\s]+)\s{3}")
    airlines_list = re.findall(pattern, paragraph)
    airlines = [airline.strip() for airline in airlines_list]
    return airlines

def departure_date(date):
    return date_conversion_function(date[0])

def departure_airport(paragraph):
    pattern = re.compile(r"From\s(.*?)\sTo")
    class_of_travel_list = re.findall(pattern, paragraph)
    return class_of_travel_list

def departure_city(paragraph):
    # not working
    pattern = re.compile(r"From\s(.*?)\sTo")
    class_of_travel_list = re.findall(pattern, paragraph)
    return [i.split(' (')[0] for i in class_of_travel_list]

def departure_time(paragraph):
    pattern = re.compile(r"Departing at (\d{2}:\d{2})")
    departure_time_list = re.findall(pattern, paragraph)
    return departure_time_list

def flight_number(paragraph):
    pattern = re.compile(r"No\s(.*?)\s+With")
    flight_number_list = re.findall(pattern, paragraph)
    return flight_number_list

def class_of_travel(paragraph):
    pattern = re.compile(r"Class (\w+)")
    class_of_travel_list = re.findall(pattern, paragraph)
    return class_of_travel_list

def arrival_airport(paragraph):
    pattern = re.compile(r"To\s(.*?)\s+Class")
    arrival_city_list = re.findall(pattern, paragraph)
    return arrival_city_list

def arrival_city(paragraph):
    pattern = re.compile(r"To\s(.*?)\s+Class")
    arrival_city_list = re.findall(pattern, paragraph)
    return [i.split(' (')[0] for i in arrival_city_list]

# def arrival_time(paragraph):
#     pattern = re.compile(r"Arriving at (\d{2}:\d{2})")
#     arrival_time_list = re.findall(pattern, paragraph)
#     return arrival_time_list

# def arrival_date(paragraph):
#     pattern = re.compile(r"Arriving\sat\s\d{2}:\d{2}\s.*?(MON \d{2} [A-Z]{3} \d{4})")
#     arrival_date_list = re.findall(pattern, paragraph)
#     return arrival_date_list

def arrival_time_and_date(paragraph):
    pattern = r"Arriving at (\d{2}:\d{2})(?: \(([^)]+)\))?"
    matches = re.findall(pattern, paragraph)

    results = []
    for match in matches:
        arrival_time = match[0]
        arrival_date = match[1] if match[1] else None
        results.append((arrival_time, arrival_date))

    return results


def airline_extraction(flight_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        if len(airline_name(paragraph)) > 0:
            flight_dict['Airline'].extend(airline_name(paragraph))
            flight_dict['Class'].extend(class_of_travel(paragraph))
            flight_dict['Departure Time'].extend(departure_time(paragraph))
            flight_dict['Departure City'].extend(departure_city(paragraph))
            flight_dict['Arrival City'].extend(arrival_city(paragraph))
            flight_dict['Flight number'].extend(flight_number(paragraph))
            flight_dict['Departure Airport'].extend(departure_airport(paragraph))
            flight_dict['Arrival Airport'].extend(arrival_airport(paragraph))

            for _ in range(len(airline_name(paragraph))):
                flight_dict['Departure Date'].append(departure_date(i))

            for dt in (arrival_time_and_date(paragraph)):
                flight_dict['Arrival Time'].append(dt[0])
                if dt [1] == None:
                    flight_dict['Arrival Date'].append(departure_date(i))
                else:
                    flight_dict['Arrival Date'].append(date_conversion_function(dt[1]))

    return flight_dict
