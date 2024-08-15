# All needed libraries
import threading
import time
import random
import os

# Importing all classes and functions from Transport
from Transport import *

'''
Contract:
        routes (dictionary): Stores routes within the transportation system by their own 'route_ID'
        vehicles (dictionary): Stores vehicles within the transportation system by their own 'vehicle_ID'
        stops (dictionary): Stores stops within the transportation system by their own 'stop_ID'

Purpose: Manage transportation routes, vehicles and stops to simulate a real-life public transportation network 
         Has functions to add/remove vehicles and routes. Updates vehicle locations and saves movements utilizing thread
         safety to support the vehicle movements, route assignments and location updates

Methods
        save_vehicle_movement: Saves the movement of each vehicle 
        add_route: Adds a new route to the transportation system 
        remove_route: Removes a route from the transportation system
        add_vehicle: Adds a vehicle to the transportation system
        remove_vehicle: Removes a vehicle from the transportation system
        assign_vehicle_to_route: Assigns a vehicle to a specific given route
        update_vehicle_location: Updates the vehicle location through a thread
        update_and_save_vehicle_location: Updates and records the movement of vehicles location in a txt file
        display_route_status: Displays the status of a given route through a thread
        search_stop: Search for a stop by it's name or stop_ID
        search_route: Search for a route by it's name or route_ID
        simulate_vehicle_movement: Simulates vehicle movements by randomly generating new coordinates for it's location
'''


class TransportManager:

    # Initialization of the TransportManager class
    def __init__(self):
        self.routes = {}  # Dictionary to hold routes
        self.vehicles = {}  # Dictionary to hold vehicles
        self.lock = threading.Lock()  # Lock for thread safety

    # Saves the vehicle movement to a file
    def save_vehicle_movement(self, vehicle_id, new_location):
        with open(self.save_file, "a") as f:  # opens the file to append
            # Writes the movement to save
            f.write(f"Vehicle {vehicle_id} moved to: Lat: {new_location[0]}, Long: {new_location[1]}\n")

    # Adds a new route to the manager
    def add_route(self, route):
        with self.lock:  # Locks thread for safety
            self.routes[route.route_id] = route  # Adds the route to the routes dictionary

    # Removes a route by its ID
    def remove_route(self, route_id):
        with self.lock:  # Locks thread for safety

            # Checks if route exists
            if route_id in self.routes:
                del self.routes[route_id]  # If route exists, delete the route
            else:
                return "Route ID not found"  # Returns error message if route not found

    # Adds a new vehicle to the manager
    def add_vehicle(self, vehicle):
        with self.lock:  # Locks thread for safety
            self.vehicles[vehicle.get_vehicle_id()] = vehicle  # Adds the vehicle to the vehicles dictionary

    # Removes vehicle by its ID
    def remove_vehicle(self, vehicle_id):
        with self.lock:  # Locks thread for safety

            # Checks if vehicle exists
            if vehicle_id in self.vehicles:
                del self.vehicles[vehicle_id]  # If vehicle exists, delete the vehicle
            else:
                return "Vehicle ID not found"  # Returns error message if vehicle not found

    # Assigns a vehicle to a given route
    def assign_vehicle_to_route(self, vehicle_id, route_id):
        with self.lock:  # Locks thread for safety

            if vehicle_id not in self.vehicles or route_id not in self.routes:  # Checks if vehicle and route exist
                return "Vehicle ID or Route ID not found"  # Returns error message if either not found

            # Adds the vehicle to the given route
            self.routes[route_id].add_vehicle(self.vehicles[vehicle_id])

    # Updates the location of the given vehicle using multi-threading
    def update_vehicle_location(self, vehicle_id, new_location):
        if vehicle_id in self.vehicles:  # Checks if the vehicle exists

            # Update the vehicle location using multi-threading
            threading.Thread(target=self.update_and_save_vehicle_location, args=(vehicle_id, new_location)).start()
            return f"Updating location for vehicle {vehicle_id}"  # Returns message updating the vehicle

        else:
            return "Vehicle ID not found"  # Return error message if vehicle ID is not found

    # Updates the vehicle location and saves the movement
    def update_and_save_vehicle_location(self, vehicle_id, new_location):
        with self.lock:  # Locks thread for safety
            if vehicle_id in self.vehicles:  # Checks if the vehicle exists
                vehicle = self.vehicles[vehicle_id]  # If exists, get the vehicle
                current_location = vehicle.get_current_location()  # Gets the current location of the vehicle
                vehicle.set_current_location(new_location)  # Updates the vehicle location to its updated position

                # Prints the updated vehicle location from last location to now
                print(f"Vehicle {vehicle_id} moved to: Lat: {new_location[0]}, Long: {new_location[1]}")

                # Save the movements to a text file
                log_dir = "vehicle_movements"  # File to save the movement txt files
                if not os.path.exists(log_dir):  # Checks if the directory exists
                    os.makedirs(log_dir)  # Creates the directory if it doesn't exist

                # Opens and creates a save txt file for the given vehicle
                with open(os.path.join(log_dir, f"{vehicle_id}_movements.txt"), "a") as save_file:
                    # Appends the movement log into the vehicles own txt file
                    save_file.write(
                        f"Moved from Lat: {current_location[0]}, Long: {current_location[1]} to Lat: {new_location[0]}, Long: {new_location[1]}\n")
            else:
                print(f"Vehicle {vehicle_id} not found")  # Prints an error message if the vehicle isn't found

    # Displays status of the given route on a new thread
    def display_route_status(self, route_id):
        def route_status():
            with self.lock:  # Locks thread for safety

                # Checks if the route exists
                if route_id in self.routes:
                    route = self.routes[route_id]  # Gets the route object
                    print(f"Route: {route.name}")  # Prints the name of the route

                    # Iterates through each vehicle assigned to the route
                    for vehicle in route.get_vehicles():
                        # Prints the details of the vehicles assigned to the given route
                        print(f"Vehicle ID: {vehicle.get_vehicle_id()}, Location: {vehicle.get_current_location()}, "
                              f"Status: {vehicle.get_status()}")
                else:
                    print("Route ID not found")  # Prints an error message if route ID is not found

        # Creates and starts a thread to display the route status
        display_thread = threading.Thread(target=route_status)
        display_thread.start()

    # Search for a stop by its name or ID
    def search_stop(self, stop_name_or_id):
        # Iterates through each route in the system
        for route_id, route in self.routes.items():

            # Iterates through each stop in the current route
            for stop in route.stops:
                # Checks if the current stop ID/Name matches what's being searched for
                if stop.stop_id == stop_name_or_id or stop.stop_name == stop_name_or_id:
                    return stop  # Returns the stop if a match is found

        return "Stop not found"  # Returns an error message if the stop is not found

    # Searches for a route or stop by its name or ID
    def search_route(self, name):
        # Iterates through each route in the system
        for route_id, route in self.routes.items():
            # Checks the current route name to see if it matches regardless of case
            if route.name.lower() == name.lower():
                return route  # Returns the route if a match is found

        return "Route not found"  # Returns an error message if the route is not found

    # Simulates vehicle movement by randomly generating locations for each vehicle and updating their locations
    def simulate_vehicle_movement(self):
        # Iterates through each vehicle in the system
        for vehicle_id, vehicle in self.vehicles.items():
            # Gets the current location from the vehicle
            current_lat, current_long = vehicle.get_current_location()

            # Updates the vehicle location randomly
            new_lat = current_lat + random.uniform(-5, 5)  # Randomly changes the lat to simulate movement
            new_long = current_long + random.uniform(-5, 5)  # Randomly changes the long to simulate movement

            # Updates the vehicle location to the new location coordinates with a thread
            self.update_vehicle_location(vehicle_id, (new_lat, new_long))


def initialize_transport_manager_from_files(vehicle_file, route_file, stops_file):
    manager = TransportManager()

    # Load vehicles from Vehicle.txt
    with open(vehicle_file, 'r') as file:  # Opens the file to read
        next(file)  # Skips the header

        # Iterates through each line in the file
        for line in file:
            vehicle_data = line.strip().split(',')  # Splits each line by commas to extract vehicle data

            # Extracts each vehicle's properties from the split data
            vehicle_id = vehicle_data[0].strip()  # Gets vehicle ID
            vehicle_type = vehicle_data[1].strip()  # Gets vehicle type
            location_lat = float(vehicle_data[2].strip())  # Gets vehicle lat coord
            location_long = float(vehicle_data[3].strip())  # Gets vehicle long coord
            status = vehicle_data[4].strip()  # Gets vehicle status

            # Creates a transport instance with the data from the file
            vehicle = Transport(vehicle_id, vehicle_type, (location_lat, location_long), status)
            manager.add_vehicle(vehicle)  # Adds the vehicle to the TransportManager

    # Load routes from Route.txt
    with open(route_file, 'r') as file:  # Opens the file to read
        next(file)  # Skips the header

        # Iterates through each line in the file
        for line in file:
            route_data = line.strip().split(',')  # Splits each line by commas to extract route data

            # Extracts each route's properties from the split data
            route_id = route_data[0].strip()  # Gets the route ID
            route_name = route_data[1].strip()  # Gets the route name
            stops = route_data[2].strip().split('|')  # Stops seperated by char '|'

            # Creates a route instance with the data from the file
            route = Route(route_id, route_name, stops)
            manager.add_route(route)  # Adds the route to the TransportManager

    # Load stops from Stops.txt
    with open(stops_file, 'r') as file:  # Opens the file to read
        next(file)  # Skips the header

        # Iterates through each line in the file
        for line in file:
            stop_data = line.strip().split(',')  # Splits each line by commas to extract stop data

            # Extracts each stop's properties from the split data
            stop_id = stop_data[0].strip()  # Gets the stop ID
            stop_name = stop_data[1].strip()  # Gets the stop name
            location_lat = float(stop_data[2].strip())  # Gets the stop lat coord
            location_long = float(stop_data[3].strip())  # Gets the stop long coord

            # Creates an instance of the stop for the TransportManager
            stop = Stop(stop_id, stop_name, (location_lat, location_long))

    return manager


if __name__ == "__main__":
    iterations = 100  # The amount of iterations to simulate the vehicle movements

    # Initializes TransportManager with data from the provided txt files
    manager = initialize_transport_manager_from_files("Vehicle.txt", "Route.txt", "Stops.txt")

    # Loops through the amount of iterations to simulate the vehicle movements
    for _ in range(iterations):
        manager.simulate_vehicle_movement()
        time.sleep(5)
