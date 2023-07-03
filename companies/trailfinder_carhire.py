import requests
import os

car_hire_dict ={'Pick up City': 'New Orleans',
                'Pick up Class': 'Airport',
                'Drop of City': 'Nashville, Tennessee',
                'Drop of Class': 'Airport',
                'pickUpDate':'2023-09-06',
                'pickUpTime': '09:00',
                'dropOffDate': '2023-09-13',
                'dropOffTime': '09:00',
                'Car name': 'Nissan rogue',
                'Vendor': 'Alamo'
               }

# search locations
def car_hire_entity_id(rental_city, rental_class):
    url = os.getenv("CARHIRE_SEARCH_LOCATION_ENDPOINT")

    querystring = {"query":rental_city}

    headers = {
        "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
        "X-RapidAPI-Host": os.getenv("SKYSCANNER_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring).json()

    pick_up_location = [i for i in response['data'] if i['class'] == rental_class]
    entity_id = pick_up_location[0]['entity_id']
    return entity_id

pick_up_entity = car_hire_entity_id(car_hire_dict["Pick up City"], car_hire_dict["Pick up Class"])
drop_of_entity = car_hire_entity_id(car_hire_dict["Drop of City"], car_hire_dict["Drop of Class"])

# search cars
url = os.getenv("SEARCH_CARS_ENDPOINT")

querystring = {"pickUpEntityId": pick_up_entity,
               "pickUpDate": car_hire_dict["pickUpDate"],
               "pickUpTime": car_hire_dict["pickUpTime"],
               "dropOffEntityId": drop_of_entity,
               "dropOffDate": car_hire_dict["dropOffDate"],
               "dropOffTime": car_hire_dict["dropOffTime"]}

headers = {
    "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
    "X-RapidAPI-Host": os.getenv("SKYSCANNER_API_HOST")
}

response = requests.get(url, headers=headers, params=querystring).json()

for i in response['data']['groups'].keys():
    if (response['data']['groups'][i]['doors'] == 'suv')\
        and (response['data']['groups'][i]['trans'] == 'automatic')\
        and (response['data']['groups'][i]['cls'] == 'intermediate')\
        and (response['data']['groups'][i]['max_seats'] == 5):
        print(response['data']['groups'][i])
        car_group = i

# select cars by company
company = [i for i in response['data']['quotes'] if i['vndr'] == car_hire_dict["Vendor"]]

# select cars by car group
group = [i for i in company if i['group'] == car_group]

# price
group[0]['price']
