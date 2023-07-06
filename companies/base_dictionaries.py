
def hotel_dict():
    hotel_dict = {'Check-in Date': [],
            'nights': [],
            'Check-out Date': [],
            'Location': [],
            'Hotel name': [],
            'Room category': [],
            'Number of rooms': [],
            'Board basis': []
            }
    return hotel_dict

def cost_dict():
    cost_dict = {'Total price': [],
            'Price per person': [],

            }
    return cost_dict

def flight_dict():
    flight_dict = {'Departure Date': [],
               'Departure Airport': [],
               'Departure City': [],
               'Departure Time': [],
               'Flight number': [],
               'Airline': [],
               'Class': [],
               'Arrival Airport': [],
               'Arrival City': [],
               'Arrival Time': [],
               'Arrival Date': []
               }
    return flight_dict

def car_hire_dict():
    car_hire_dict ={'Pick up City': [],
                'Pick up Class': [],
                'Drop of City': [],
                'Drop of Class': [],
                'pickUpDate': [],
                'pickUpTime': [],
                'dropOffDate': [],
                'dropOffTime': [],
                'Car name': [],
                'Vendor': [],
                'Transmission': [], # Automatic
                'Max seats': [],
                'Car class': [], #intermediate
                'Car type': [] # SUV
               }

    return car_hire_dict

def excursion_dict():
    excursion_dict ={'Excursion Name': [],
                'Location': [],
                'Operator': [],
                'Description': []
               }

    return excursion_dict
