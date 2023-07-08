import re
# from companies..helper.trailfinders_helper_functions import date_conversion_function
import datetime
from helper.trailfinders_helper_functions import date_conversion_function

car_hire_dict = {'Pick up City': [],
                'Pick up Class': [],
                'Drop of City': [],
                'Drop of Class': [],
                'pickUpDate': [],
                'pickUpTime': [],
                'dropOffDate': [],
                'dropOffTime': [],
                'Car name': [],
                'Vendor': [],
                'Transmission': [], # Automatic
                'Max seats': [],
                'Car class': [], #intermediate
                'Car type': []# suv
}

def regex_function(regex, paragraph):
    match = regex.search(paragraph)
    variable = None
    if match:
        variable = match.group(1).strip()
    return variable

def pick_up_city(paragraph):
    regex = re.compile(r"Pick up:\s+(.+?)\s{3}", re.MULTILINE)
    return regex_function(regex, paragraph)

def pick_up_class(paragraph):
    regex = re.compile(r"Pick up location:\s+(.+?)\s{3}", re.MULTILINE)
    return regex_function(regex, paragraph)

def drop_of_city(paragraph):
    regex = re.compile(r"Drop off:\s+(.+?)\s{3}", re.MULTILINE)
    return regex_function(regex, paragraph)

def drop_of_class(paragraph):
    regex = re.compile(r"Drop off location:\s+(.+?)\s{3}", re.MULTILINE)
    return regex_function(regex, paragraph)

def pick_up_date(i):
    return date_conversion_function(i[0])

def pick_up_time(paragraph):
    regex = re.compile(r"Pick up .+ - (\d{2}:\d{2})", re.MULTILINE)
    return regex_function(regex, paragraph)

def drop_of_date(paragraph):
    regex = re.compile(r"Drop off time: (\d{2} \w+ \d{4})")
    origional_date_format = regex_function(regex, paragraph)
    date_object = datetime.datetime.strptime(origional_date_format, "%d %b %Y")
    return date_object.strftime("%Y-%m-%d")


def drop_of_time(paragraph):
    regex = re.compile(r"at (\d{2}:\d{2})")
    return regex_function(regex, paragraph)

def car_name(paragraph):
    regex = re.compile(r"\s{2}([^:]+) or similar", re.MULTILINE)
    return regex_function(regex, paragraph)

def vendor(paragraph):
    regex = re.compile(r"Supplier: (\w+)", re.MULTILINE)
    return regex_function(regex, paragraph)

def transmission():
    pass

def max_seats():
    pass

def car_class():
    pass

def car_type():
    pass


def car_hire_extraction(car_hire_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        if vendor(paragraph) != None:
            print(paragraph)
            print(pick_up_date(i))
            print(vendor(paragraph))
            print(pick_up_time(paragraph))
            print(pick_up_city(paragraph))
            print(pick_up_class(paragraph))
            print(drop_of_city(paragraph))
            print(drop_of_class(paragraph))
            print(drop_of_date(paragraph))
            print(drop_of_time(paragraph))
            print(car_name(paragraph))

    return car_hire_dict
