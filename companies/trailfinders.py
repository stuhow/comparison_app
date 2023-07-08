import re

import pdftotext
from base_dictionaries import hotel_dict, flight_dict, cost_dict, car_hire_dict, excursion_dict
from hotel.trainfinders_hotel_functions import hotel_extraction
from helper.trailfinders_helper_functions import load_text, extract_date_tuples
from cost.trailfinders_costs import extract_costs
from flight.trailfinders_flights_functions import airline_extraction
from car_hire.trailfinders_car_hire_functions import car_hire_extraction
from excursion.trailfinders_excursions import excursion_extraction

# from companies.dictionaries import hotel_dict, flight_dict, cost_dict
# from companies.hotel.trainfinders_hotel_functions import hotel_extraction
# from companies.helper.trailfinders_helper_functions import load_text, extract_date_tuples
# from companies.cost.trailfinders_costs import extract_costs
# from companies.flight.trailfinders_flights_functions import airline_extraction
# from companies.car_hire.trailfinders_car_hire_functions import car_hire_extraction

def trailfinders_dictionaries(text):

    # load the text
    # text = load_text(pdf)

    # import standard costs dictionary
    cost_dictionary = cost_dict()

    # extracting costs
    costs_dict = extract_costs(text, cost_dictionary)

    # import standard hotel & cost dictionary
    base_hotel_dict = hotel_dict()
    base_flight_dict = flight_dict()
    base_car_hire_dict = car_hire_dict()
    base_excursion_dict = excursion_dict()

    # extract the list of date tuples from the text
    tuple_dates_list = extract_date_tuples(text)

    # loop through the date tuples to extract the info for each day
    for i in tuple_dates_list:

        # find details in the text between dates
        if len(i)==2:
            inbetween_dates_pattern = re.compile('(\s' + i[0]  + ')((.|\n)*)' + '(\s' + i[1] + ')')

            # get hotel dictionary
            new_hotel_dict = hotel_extraction(base_hotel_dict, inbetween_dates_pattern, text, i)
            new_flight_dict = airline_extraction(base_flight_dict, inbetween_dates_pattern, text, i)
            new_car_hire_dict = car_hire_extraction(base_car_hire_dict, inbetween_dates_pattern, text, i)
            new_excursion_dict = excursion_extraction(base_excursion_dict, inbetween_dates_pattern, text, i)

        # find details after final date
        else:
            final_date_pattern = re.compile('( ' + i[0]  + ')((.|\n)*)')

            # get hotel dictionary
            new_hotel_dict = hotel_extraction(base_hotel_dict, final_date_pattern, text, i)
            new_flight_dict = airline_extraction(base_flight_dict, final_date_pattern, text, i)
            new_car_hire_dict = car_hire_extraction(base_car_hire_dict, final_date_pattern, text, i)
            new_excursion_dict = excursion_extraction(base_excursion_dict, inbetween_dates_pattern, text, i)

    return costs_dict, new_hotel_dict, new_flight_dict, new_car_hire_dict, new_excursion_dict


pdf_file = open('trailfinders.pdf', 'rb')
full_pdf = pdftotext.PDF(pdf_file)

text =''
for page in full_pdf:
    text += page

gf = trailfinders_dictionaries(text)
print(gf)
