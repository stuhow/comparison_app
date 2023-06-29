import re
from dictionaries import hotel_dict, flight_dict, cost_dict
from trainfinders_hotel_functions import hotel_extraction
from trailfinders_helper_functions import load_text, extract_date_tuples
from trailfinders_costs import extract_costs
from trailfinders_flights_functions import airline_extraction

def trailfinders_dictionaries():
    # load the text
    text =load_text()

    # import standard costs dictionary
    cost_dictionary = cost_dict()

    # extracting costs
    costs_dict = extract_costs(text, cost_dictionary)

    # import standard hotel & cost dictionary
    base_hotel_dict = hotel_dict()
    base_flight_dict = flight_dict()

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

        # find details after final date
        else:
            final_date_pattern = re.compile('( ' + i[0]  + ')((.|\n)*)')

            # get hotel dictionary
            new_hotel_dict = hotel_extraction(base_hotel_dict, final_date_pattern, text, i)
            new_flight_dict = airline_extraction(base_flight_dict, final_date_pattern, text, i)

    return costs_dict, new_hotel_dict, new_flight_dict

gf= trailfinders_dictionaries()
print(gf[2])
