import os
import requests

hotel_dict = {'Check-in Date': ['2023-09-08', '2023-09-11', '2023-09-12', '2023-09-15'],
              'nights': ['3', '1', '3', '2'],
              'Check-out Date': ['2023-09-11', '2023-09-12', '2023-09-15', '2023-09-17'],
              'Location': ['NEW ORLEANS, LOUISIANA', 'NATCHEZ, MISSISSIPPI', 'MEMPHIS, TENNESSEE', 'NASHVILLE, TENNESSEE'],
              'Hotel name': ['THE ELIZA JANE', 'NATCHEZ GRAND HOTEL', 'HYATT CENTRIC BEALE STREET MEMPHIS', 'HOLSTON HOUSE NASHVILLE'],
              'Room category': ['ONE KING BED', 'DELUXE HISTORIC VIEW ROOM (MAX OCC. 2)', '1 KING BED', 'KING ROOM'],
              'Number of rooms': ['1 DOUBLE OCCUPANCY', '1 DOUBLE OCCUPANCY', '1 DOUBLE OCCUPANCY', '1 DOUBLE OCCUPANCY'],
              'Board basis': ['INCLUDES BREAKFAST FOR 2 ADULTS', '1 KING (AMERICAN BREAKFAST)', 'INCLUDES BREAKFAST FOR 2 ADULTS', 'No meals included']}

for i in range(len(hotel_dict['Check-in Date'])):
    print(i)
    full_hotel_name = hotel_dict['Hotel name'][i] + ", " + hotel_dict['Location'][i]
    print(full_hotel_name)
    url = os.getenv("HOTEL_LOCATION_ENDPOINT")

    querystring = {"name":full_hotel_name[:50:],
                    "locale":"en-gb"}

    headers = {
        "X-RapidAPI-Key": os.getenv("BOOKING_API_KEY"),
        "X-RapidAPI-Host": os.getenv("BOOKING_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring)

    response= response.json()

    hotel_id = response[0]['dest_id']
    print(hotel_id)

    url = os.getenv("HOTEL_SEARCH_ENDPOINT")

    querystring = {"order_by":"popularity",
                    "adults_number":"2",
                    "checkin_date":hotel_dict['Check-in Date'][i],
                    "filter_by_currency":"GBP",
                    "dest_id":hotel_id,
                    "locale":"en-gb",
                    "checkout_date":hotel_dict['Check-out Date'][i],
                    "units":"metric",
                    "room_number":"1",
                    "dest_type":"hotel"}

    headers = {
        "X-RapidAPI-Key": os.getenv("BOOKING_API_KEY"),
        "X-RapidAPI-Host": os.getenv("BOOKING_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring).json()

    total_price = None
    if response['results'][0]['priceBreakdown'] == None:
        total_price = 'Sold out on booking.com'
    else:
        grossPrice = response['results'][0]['priceBreakdown']['grossPrice']['value']

        if 'excludedPrice' in response['results'][0]['priceBreakdown'].keys():
            excludedPrice = response['results'][0]['priceBreakdown']['excludedPrice']['value']
            total_price = round(excludedPrice + grossPrice)
        else:
            total_price = round(grossPrice)

    review_score = response['results'][0]['reviewScore']

    if 'Starting price on Booking.com' not in hotel_dict.keys():
        hotel_dict['Starting price on Booking.com'] = [total_price]
    else:
        hotel_dict['Starting price on Booking.com'].append(total_price)

    if 'Review score on Booking.com' not in hotel_dict.keys():
        hotel_dict['Review score on Booking.com'] = [review_score]
    else:
        hotel_dict['Review score on Booking.com'].append(review_score)

    print(hotel_dict)
