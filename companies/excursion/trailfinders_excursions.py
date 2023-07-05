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


def excursion_extraction(flight_dict, pattern, text, i):
    matches = pattern.finditer(text)
    for match in matches:
        paragraph = match.group(2)

    return flight_dict
