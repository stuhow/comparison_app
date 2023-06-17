import re
from datetime import datetime, timedelta

# client details
def abercrombie_dictionaries(text):
    # a function to extract dictionaries for costs, flights and hotels

    date_pattern = re.compile(r'[A-Z]+[a-z]*\s[0-9]{1,2}[a-z]+\s[a-zA-Z]+\s[0-9]{4}')
    hotel_pattern = re.compile('(.+)([0-9]+).Night(s).+\n([0-9]+)\sx\s(.+)(\sRoom.+)\n')
    flight_pattern = re.compile('(Depart:)((.|\n)*)(Flight No:)((.|\n)*)(Flight Class:)((.|\n)*)(Arrive:)((.|\n)*)(Duration:)(.+)')
    cost_pattern = re.compile('Total Holiday Cost   Average per person cost   Total Deposit required to confirm \nthese arrangements  \n \n(£.+)\n.+\n(£.+)\n(£.+)')
    date_format ="%A.%dth.%B.%Y"

    # create list of dates
    matches1 = date_pattern.finditer(text)
    dates_list=[]
    for match1 in matches1:
        dates_list.append(match1.group().replace(' ','.'))


    # Create date ranges to find the paragraphs of text
    tuple_dates_list = [(x,y) for x,y in zip(dates_list, dates_list[1:])]
    tuple_dates_list.append((dates_list[-1],)) # finds text after the final date


    #create dict with date as key and hotel/flight details as a list
    hotel_dict = {'Check-in Date': [],
                'nights': [],
                'Check-out Date': [],
                'Hotel name': [],
                'Room category': [],
                'Number of rooms': [],
                'Board basis': []
                }

    flight_dict ={'Departure Date': [],
                'Departure Airport': [],
                'Departure City': [],
                'Departure Time': [],
                'Flight number': [],
                'Airline': [],
                'Class': [],
                'Arival Airport': [],
                'Arrival City': [],
                'Arrival Time': [],
                'Arrival Date': [],
                'Duration': []
            }

    # Loop over date ranges in the tuples to extract the text between dates and after the final date
    for i in tuple_dates_list:
        # find's text between dates
        if len(i)==2:
            hotel_pattern2 = re.compile('(' + i[0]  + ')((.|\n)*)' + i[1])
            matches = hotel_pattern2.finditer(text)
            for match in matches:
                paragraph = match.group(2)

                # Extract hotel details
                hotel = re.findall(hotel_pattern, paragraph)
                if len(hotel) > 0:
                    hotel_dict['Check-in Date'].append(i[0])
                    hotel_dict['nights'].append(hotel[0][1])
                    new_date = datetime.strptime(i[0], date_format) + timedelta(days=int(hotel[0][1]))
                    hotel_dict['Check-out Date'].append(new_date.strftime(date_format))
                    hotel_dict['Hotel name'].append(hotel[0][0].strip())
                    hotel_dict['Room category'].append(hotel[0][4].replace(' for 2 Adults','').strip())
                    hotel_dict['Number of rooms'].append(hotel[0][3])
                    hotel_dict['Board basis'].append(hotel[0][5].strip())

                # Extract flight details if the exist
                flight = re.findall(flight_pattern, paragraph)
                if len(flight) > 0:
                    flight_dict['Departure Date'].append(i[0])
                    flight_dict['Departure Airport'].append(flight[0][1].strip().split(', ')[0])
                    flight_dict['Departure City'].append(flight[0][1].split(', ')[1])
                    flight_dict['Departure Time'].append(flight[0][1].split(', ')[-1].replace('at ','').strip())
                    flight_dict['Flight number'].append(flight[0][4].strip().split(' ')[0])
                    flight_dict['Airline'].append(flight[0][4].split('(')[1].split(')')[0])
                    flight_dict['Class'].append(flight[0][7].strip().split('(')[1].split(')')[0])
                    flight_dict['Arival Airport'].append(flight[0][10].strip().split(', ')[0])
                    flight_dict['Arrival City'].append(flight[0][10].strip().split(', ')[1])
                    flight_dict['Arrival Time'].append(flight[0][10].strip().split(', ')[-1].replace('at ','').split(' on ')[0])
                    flight_dict['Arrival Date'].append(flight[0][10].strip().split(', ')[-1].replace('at ','').split(' on ')[1])
                    flight_dict['Duration'].append(flight[0][-1].strip())

        else:
            hotel_pattern2 = re.compile('(' + i[0]  + ')((.|\n)*)')
            matches = hotel_pattern2.finditer(text)

            for match in matches:
                paragraph = match.group(2)

                # extract hotel details if they exist
                hotel = re.findall(hotel_pattern, paragraph)
                if len(hotel) > 0:
                    hotel_dict['Check-in Date'].append(i[0])
                    hotel_dict['nights'].append(hotel[0][1])
                    new_date = datetime.strptime(i[0], date_format) + timedelta(days=int(hotel[0][1]))
                    hotel_dict['Check-out Date'].append(new_date.strftime(date_format))
                    hotel_dict['Hotel name'].append(hotel[0][0].strip())
                    hotel_dict['Room category'].append(hotel[0][4].replace(' for 2 Adults','').strip())
                    hotel_dict['Number of rooms'].append(hotel[0][3])
                    hotel_dict['Board basis'].append(hotel[0][5].strip())

                # Extract flight details if the exist
                flight = re.findall(flight_pattern, paragraph)
                if len(flight) > 0:
                    flight_dict['Departure Date'].append(i[0])
                    flight_dict['Departure Airport'].append(flight[0][1].strip().split(', ')[0])
                    flight_dict['Departure City'].append(flight[0][1].split(', ')[1])
                    flight_dict['Departure Time'].append(flight[0][1].split(', ')[-1].replace('at ','').strip())
                    flight_dict['Flight number'].append(flight[0][4].strip().split(' ')[0])
                    flight_dict['Airline'].append(flight[0][4].split('(')[1].split(')')[0])
                    flight_dict['Class'].append(flight[0][7].strip().split('(')[1].split(')')[0])
                    flight_dict['Arival Airport'].append(flight[0][10].strip().split(', ')[0])
                    flight_dict['Arrival City'].append(flight[0][10].strip().split(', ')[1])
                    flight_dict['Arrival Time'].append(flight[0][10].strip().split(', ')[-1].replace('at ','').split(' on ')[0])
                    flight_dict['Arrival Date'].append(flight[0][10].strip().split(', ')[-1].replace('at ','').split(' on ')[1])
                    flight_dict['Duration'].append(flight[0][-1].strip())


    # Find trip cost

    costs = re.findall(cost_pattern, text)

    cost_dict = {'Breakdown': ['Total Holiday Cost', 'Average per person cost', 'Total Deposit required to confirm these arrangements'], 'Cost': [costs[0][0].split(' ')[0], costs[0][1], costs[0][2]]}

    return cost_dict, hotel_dict, flight_dict
