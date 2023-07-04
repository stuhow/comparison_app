import re
# from companies.trailfinders_helper_functions import date_conversion_function

from trailfinders_helper_functions import date_conversion_function



def car_hire_extraction(hotel_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        print(paragraph)

    return hotel_dict
