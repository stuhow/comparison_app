import os
import requests


def add_hotel_details(hotel_dict):
    for i in range(len(hotel_dict['Check-in Date'])):

        full_hotel_name = hotel_dict['Hotel name'][i] + ", " + hotel_dict['Location'][i]

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

    return hotel_dict
