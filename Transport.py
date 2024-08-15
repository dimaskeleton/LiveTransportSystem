"""
Contract: Represent a transportation system with a unique identifier, type, location, and status
Purpose:
    - Provide the structure for all the transportation methods
    - Verifies each vehicle has its own identification
    - Also verifies each vehicle has its associated stats
"""


class Transport:
    # Encapsulation
    def __init__(self, vehicle_id, vehicle_type, current_location, status):
        # Initializes a Transport object with ID, type, location, and status
        self.__vehicle_id = vehicle_id
        self.__vehicle_type = vehicle_type
        self.__current_location = current_location
        self.__status = status

    # Updates the status of the transport system
    def update_status(self, new_status):
        self.status = new_status

    # Getters and Setters (Encapsulation)
    def get_vehicle_id(self):
        return self.__vehicle_id  # Return the vehicle ID

    # Getters and Setters (Encapsulation)
    def get_vehicle_type(self):
        return self.__vehicle_type  # Return the vehicle type

    # Getters and Setters (Encapsulation)
    def get_current_location(self):
        return self.__current_location  # Return the vehicle location

    # Getters and Setters (Encapsulation)
    def set_current_location(self, new_location):
        self.__current_location = new_location  # Update the vehicle location

    # Getters and Setters (Encapsulation)
    def get_status(self):
        return self.__status  # Return status of the vehicle

    # Getters and Setters (Encapsulation)
    def set_status(self, new_status):
        self.__status = new_status  # Update the status of the vehicle


'''
Contract: Represent a stop/station within a transportation network
Purpose:
    - Create a stop with a unique identifier, name, and location
    - Allow for easy identification and differentiation between the stops
'''


class Stop:
    # Encapsulation
    def __init__(self, stop_id, stop_name, location):
        # Initializes a Stop object with ID, name, and location
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.location = location  # Tuple for x and y axis


'''
Contract: Represent a line within a transportation network 
Purpose:
    - Track vehicles on a given route
    - Manage list of stops on the route
    - Differentiate routes with ID, Name, and Stops 
'''


class Route:
    def __init__(self, route_id, name, stops):
        # Initializes a Route line with ID, name, and stops
        self.route_id = route_id
        self.name = name
        self.stops = stops  # List of stops that will be on a route
        self.vehicles = []  # Vehicles assigned to the current route
        self.status = "On Time"  # Default status property

    # Updates the status of the route
    def update_status(self, new_status):
        self.status = new_status

    # Adds a vehicle to the route
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    # Removes a vehicle from the route by its ID
    def remove_vehicle(self, vehicle_id):
        self.vehicles = [v for v in self.vehicles if v.get_vehicle_id() != vehicle_id]

    # Returns the list of vehicles currently on the route
    def get_vehicles(self):
        return self.vehicles

    def get_status(self):
        return self.status


'''
Contract: Extends the Transport class to a bus form of transportation
Purpose:
    - Initialize a new vehicle bus 
    - Inherits the functionality of the Transport class for vehicle specific methods
'''


class Bus(Transport):
    def __init__(self, vehicle_id, current_location, status):
        super().__init__(vehicle_id, "Bus", current_location, status)


'''
Contract: Extends the Transport class to a Train form of transportation
Purpose:
    - Initialize a new vehicle Train 
    - Inherits the functionality of the Transport class for vehicle specific methods
'''


class Train(Transport):
    def __init__(self, vehicle_id, current_location, status):
        super().__init__(vehicle_id, "Train", current_location, status)


'''
Contract: Extends the Transport class to a Uber form of transportation
Purpose:
    - Initialize a new vehicle Uber 
    - Inherits the functionality of the Transport class for vehicle specific methods
'''


class Uber(Transport):
    def __init__(self, vehicle_id, current_location, status):
        super().__init__(vehicle_id, "Uber", current_location, status)
