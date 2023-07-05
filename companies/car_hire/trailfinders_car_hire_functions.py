import re
# from companies..helper.trailfinders_helper_functions import date_conversion_function

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

def pick_up_city():
    pass

def pick_up_class():
    pass

def drop_of_city():
    pass

def drop_of_class():
    pass

def pick_up_date():
    pass

def pick_up_time():
    pass

def drop_of_date():
    pass

def drop_of_time():
    pass

def car_name():
    pass

def vendor():
    pass

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
        print(paragraph)

    return car_hire_dict
