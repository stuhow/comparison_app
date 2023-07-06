import re

def arrival_time_and_date(paragraph):
    pattern = r"Arriving at (\d{2}:\d{2})(?: \(([^)]+)\))?"
    matches = re.findall(pattern, paragraph)

    results = []
    for match in matches:
        arrival_time = match[0]
        arrival_date = match[1] if match[1] else None
        results.append((arrival_time, arrival_date))

    return results


excursion_dict ={'Excursion Name': [],
                'Location': [],
                'Operator': [],
                'Description': []
               }


def excursion_name():
    pass

def location():
    pass

def operator():
    pass

def tour_description():
    pass


def excursion_extraction(excursion_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)

    return excursion_dict
