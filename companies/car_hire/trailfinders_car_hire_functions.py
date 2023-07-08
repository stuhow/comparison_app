import re
from companies.helper.trailfinders_helper_functions import date_conversion_function
import datetime
# from helper.trailfinders_helper_functions import date_conversion_function

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


def extract_text(input_text, start_pattern, check_word):
    # Create the regular expression pattern
    pattern = f"{re.escape(start_pattern)}(.*?)\s{3}"

    text = ''
    # Find all matches
    matches = re.findall(pattern, input_text, re.DOTALL)
    first_line = matches[0].split("\n")[0].split("   ")[0]
    if matches[0].split("\n")[1].strip().split("   ")[0].startswith(check_word):
        text = first_line
    else:
        text = first_line + " " + matches[0].split("\n")[1].strip().split("   ")[0]

    return text

def transmission(text):
    if 'Automatic' in text:
        return 'Automatic'

def max_seats():
    pass

def car_class(text):
    if 'Intermediate' in text:
        return 'Intermediate'

def car_type(text):
    if 'SUV' in text:
        return 'SUV'


def car_hire_extraction(car_hire_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        if vendor(paragraph) != None:

            text = extract_text(paragraph, 'Car type: ', 'Pick up:')

            car_hire_dict['Pick up City'].append(pick_up_city(paragraph))
            car_hire_dict['Pick up Class'].append(pick_up_class(paragraph))
            car_hire_dict['Drop of City'].append(drop_of_city(paragraph))
            car_hire_dict['Drop of Class'].append(drop_of_class(paragraph))
            car_hire_dict['pickUpDate'].append(pick_up_date(i))
            car_hire_dict['pickUpTime'].append(pick_up_time(paragraph))
            car_hire_dict['dropOffDate'].append(drop_of_date(paragraph))
            car_hire_dict['dropOffTime'].append(drop_of_time(paragraph))
            car_hire_dict['Car name'].append(car_name(paragraph))
            car_hire_dict['Vendor'].append(vendor(paragraph))
            car_hire_dict['Transmission'].append(transmission(text))
            car_hire_dict['Car class'].append(car_class(text))
            car_hire_dict['Car type'].append(car_type(text))

    return car_hire_dict
