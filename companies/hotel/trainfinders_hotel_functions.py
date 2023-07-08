import re
from companies.helper.trailfinders_helper_functions import date_conversion_function

# from helper.trailfinders_helper_functions import date_conversion_function

def regex_function(regex, paragraph):
    match = regex.search(paragraph)
    variable = None
    if match:
        variable = match.group(1).strip()
    return variable

def accomedation_name(paragraph):
    regex = re.compile(r'ACCOMMODATION\s+(.*)\s+Location', re.DOTALL)
    return regex_function(regex, paragraph)

def number_of_nights(paragraph):
    regex = re.compile(r'for\s+(\d+)\s+night')
    return regex_function(regex, paragraph)

def check_in_date(i):
    return date_conversion_function(i[0])

def check_out_date(paragraph):
    regex = re.compile(r'Check out:\s+([A-Z]{3}\s+\d{1,2}\s+[A-Z]{3}\s+\d{4})')
    return date_conversion_function(regex_function(regex, paragraph))

def number_of_rooms(paragraph):
    regex = re.compile(r'Accommodation type:\s+(.*)')
    return regex_function(regex, paragraph)

def room_type(paragraph):
    # a function to extract the room type from the quote
    # from which you can extract the room category and board basis
    regex = re.compile(r'Room type:\s+(.*?)\s+Accommodation type:', re.DOTALL)
    return regex_function(regex, paragraph)

def room_category(room_type_text):
    if ' - ' in room_type_text:
        return room_type_text.split(' - ')[0].replace("\n", "")
    else:
        return room_type_text.strip()

def board_basis(room_type_text):
    if ' - ' in room_type_text:
        trimmed_string=  room_type_text.split(' - ')[1].replace("\n", "").strip()
        return " ".join(trimmed_string.split())
    else:
        return 'No meals included'

def hotel_location(paragraph):
    regex = re.compile(r'Location\s+(.*?)(?:\r?\n|$)')
    return regex_function(regex, paragraph)

def hotel_extraction(hotel_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        if accomedation_name(paragraph) != None:
            hotel_dict['Hotel name'].append(accomedation_name(paragraph))
            hotel_dict['Check-in Date'].append(check_in_date(i))
            hotel_dict['Number of rooms'].append(number_of_rooms(paragraph))
            hotel_dict['nights'].append(number_of_nights(paragraph))
            hotel_dict['Check-out Date'].append(check_out_date(paragraph))
            room_type_text = room_type(paragraph)
            hotel_dict['Room category'].append(room_category(room_type_text))
            hotel_dict['Board basis'].append(board_basis(room_type_text))
            hotel_dict['Location'].append(hotel_location(paragraph))
    return hotel_dict
