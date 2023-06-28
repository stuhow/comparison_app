import re
from dictionaries import hotel_dict
from trainfinders_hotel_functions import hotel_extraction
from trailfinders_helper_functions import load_text, extract_date_tuples
from trailfinders_costs import extract_costs

def trailfinders_dictionaries():
    # load the text
    text =load_text()

    # extracting costs
    costs_dict = extract_costs(text)

    # import standard hotel dictionary
    base_hotel_dict = hotel_dict()

    # extract the list of date tuples from the text
    tuple_dates_list = extract_date_tuples(text)

    # loop through the date tuples to extract the info for each day
    for i in tuple_dates_list:

        # find details in the text between dates
        if len(i)==2:
            inbetween_dates_pattern = re.compile('(\s' + i[0]  + ')((.|\n)*)' + '(\s' + i[1] + ')')

            # get hotel dictionary
            single_hotel_dict = hotel_extraction(base_hotel_dict, inbetween_dates_pattern, text, i)

        # find details after final date
        else:
            final_date_pattern = re.compile('( ' + i[0]  + ')((.|\n)*)')

            # get hotel dictionary
            single_hotel_dict = hotel_extraction(base_hotel_dict, final_date_pattern, text, i)

    return costs_dict, single_hotel_dict

gf= trailfinders_dictionaries()
print(gf)
