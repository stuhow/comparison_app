import re

from helper.trailfinders_helper_functions import date_conversion_function

excursion_dict ={'Excursion Name': [],
                'Location': [],
                'Operator': [],
                'Description': []
               }


def excursion_name(paragraph):
    pattern = re.compile(r"^(.*?)Departing from", re.MULTILINE)
    excursion_name_list = re.findall(pattern, paragraph)
    return [i.strip() for i in excursion_name_list]

def excursion_start_date(i):
    return(date_conversion_function(i[0]))


def location(paragraph):
    pattern = re.compile(r"^.*Departing from ([^\n]+)", re.MULTILINE)
    location_name_list = re.findall(pattern, paragraph)
    return [i.strip() for i in location_name_list]

def operator(paragraph):
    pattern = re.compile(r"^.*With (\w+(?: \w+)*)$", re.MULTILINE)
    operator_name_list = re.findall(pattern, paragraph)
    return [i.strip() for i in operator_name_list]

def tour_description(paragraph):
    pattern = re.compile(r"Tour copy supplied by [^:]+:\n([\s\S]+?)(?:Your tour voucher will be available|\n\n)", re.MULTILINE)
    tour_description_list = re.findall(pattern, paragraph)
    return [i.strip().replace("\n       "," ") for i in tour_description_list]


def excursion_extraction(excursion_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)
        if len(excursion_name(paragraph)) > 0:
            if excursion_name(paragraph)[0] != "":
                dates_list = [excursion_start_date(i) for _ in range(len(excursion_name(paragraph)))]
                print(dates_list)
                print(excursion_name(paragraph))
                print(location(paragraph))
                print(operator(paragraph))
                print(tour_description(paragraph))


    return excursion_dict
