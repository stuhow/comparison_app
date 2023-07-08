import re

def regex_function(regex, paragraph):
    match = regex.search(paragraph)
    variable = None
    if match:
        variable = match.group(1).strip()
    return float(variable)

def total_trip_cost(text):
    regex = re.compile(r'Inclusive price\s+£(\d+\.\d{2})')
    return regex_function(regex, text)

def number_of_people(text):
    pattern = r"Prepared for:(.*?)IMPORTANT INFORMATION"
    match = re.search(pattern, text, re.DOTALL)
    lines_between = match.group(1).strip().split('\n')
    return len(lines_between)

def cost_per_person(text):
    return total_trip_cost(text)/number_of_people(text)

def extract_costs(text, cost_dictionary):
    cost_dictionary['Total price'].append(total_trip_cost(text))
    cost_dictionary['Price per person'].append(cost_per_person(text))
    cost_dictionary['Number of people'].append(number_of_people(text))
    return cost_dictionary
