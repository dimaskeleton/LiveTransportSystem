from TransportManager import *

# Tests for all the methods in TransportManager

def test_transport_initialization():
    vehicle = Transport("Vehicle1", "Bus", (40.7, -67.4), "On Time")

    assert vehicle.get_vehicle_id() == "Vehicle1"
    assert vehicle.get_vehicle_type() == "Bus"
    assert vehicle.get_current_location() == (40.7, -67.4)
    assert vehicle.get_status() == "On Time"


def test_set_current_location():
    vehicle = Transport("Vehicle1", "Bus", (40.7, -67.4), "On Time")

    new_location = (40.715, -74.01)
    vehicle.set_current_location(new_location)

    assert vehicle.get_current_location() == new_location


def test_set_status():
    vehicle = Transport("Vehicle1", "Bus", (40.7, -67.4), "On Time")

    new_status = "Delayed"
    vehicle.set_status(new_status)

    assert vehicle.get_status() == new_status


def test_stop_initialization():
    stop = Stop("stop1", "Park Street", (40.7, -67.4))

    assert stop.stop_id == "stop1"
    assert stop.stop_name == "Park Street"
    assert stop.location == (40.7, -67.4)


def test_route_initialization():
    stops = ["Stop1", "Stop2", "Stop3"]
    route = Route("route1", "Route 1", stops)

    assert route.route_id == "route1"
    assert route.name == "Route 1"
    assert len(route.stops) == 3
    assert route.stops[0] == "Stop1"
    assert len(route.vehicles) == 0


def test_add_vehicle():
    stops = ["Stop1", "Stop2", "Stop3"]
    route = Route("route1", "Route 1", stops)
    vehicle = Transport("Vehicle1", "Bus", (40.7, -67.4), "On Time")

    route.add_vehicle(vehicle)

    assert len(route.vehicles) == 1
    assert route.vehicles[0].get_vehicle_id() == "Vehicle1"


def test_remove_vehicle():
    stops = ["Stop1", "Stop2", "Stop3"]
    route = Route("route1", "Route 1", stops)

    vehicle1 = Transport("Vehicle1", "Bus", (40.7, -67.4), "On Time")
    vehicle2 = Transport("Vehicle2", "Bus", (29.2, -67.4), "Delayed")

    route.add_vehicle(vehicle1)
    route.add_vehicle(vehicle2)

    route.remove_vehicle("Vehicle1")

    assert len(route.vehicles) == 1
    assert route.vehicles[0].get_vehicle_id() == "Vehicle2"


def test_get_vehicles():
    stops = ["Stop1", "Stop2", "Stop3"]
    route = Route("route1", "Route 1", stops)

    vehicle1 = Transport("Vehicle1", "Bus", (40.7, -67.4), "On Time")
    vehicle2 = Transport("Vehicle2", "Bus", (29.2, -67.4), "Delayed")

    route.add_vehicle(vehicle1)
    route.add_vehicle(vehicle2)

    vehicles = route.get_vehicles()

    assert len(vehicles) == 2
    assert vehicles[0].get_vehicle_id() == "Vehicle1"
    assert vehicles[1].get_vehicle_id() == "Vehicle2"


def test_bus_initialization():
    bus = Bus("Bustop1", (40.7, -67.4), "On Time")

    assert bus.get_vehicle_id() == "Bustop1"
    assert bus.get_vehicle_type() == "Bus"
    assert bus.get_current_location() == (40.7, -67.4)
    assert bus.get_status() == "On Time"


def test_train_initialization():
    train = Train("Train1", (29.2, -67.4), "On Time")

    assert train.get_vehicle_id() == "Train1"
    assert train.get_vehicle_type() == "Train"
    assert train.get_current_location() == (29.2, -67.4)
    assert train.get_status() == "On Time"


def test_uber_initialization():
    uber = Uber("Uberoute1", (47.5, -67.4), "Available")

    assert uber.get_vehicle_id() == "Uberoute1"
    assert uber.get_vehicle_type() == "Uber"
    assert uber.get_current_location() == (47.5, -67.4)
    assert uber.get_status() == "Available"


def test_add_and_remove_route():
    transport_manager = TransportManager()
    route = Route("route1", "Route 1", ["Stop1", "Stop2"])

    transport_manager.add_route(route)
    assert "route1" in transport_manager.routes

    transport_manager.remove_route("route1")
    assert "route1" not in transport_manager.routes

    transport_manager.remove_route("route2")
    assert "route2" not in transport_manager.routes


def test_add_and_remove_vehicle():
    transport_manager = TransportManager()
    vehicle = Transport("Vehicle1", "Bus", (0, 0), "On Time")

    transport_manager.add_vehicle(vehicle)
    assert "Vehicle1" in transport_manager.vehicles

    transport_manager.remove_vehicle("Vehicle1")
    assert "Vehicle1" not in transport_manager.vehicles

    transport_manager.remove_vehicle("Vehicle2")
    assert "Vehicle2" not in transport_manager.vehicles


def test_assign_vehicle_to_route():
    manager = TransportManager()
    route1 = Route("Route1", "First Route", [Stop("stop1", "Stop One", (0, 0))])
    bus = Transport("Bustop1", "Bus", (0, 0), "On Time")

    manager.add_route(route1)
    manager.add_vehicle(bus)

    manager.assign_vehicle_to_route("Bustop1", "Route1")
    assert bus in manager.routes["Route1"].get_vehicles()

    manager.assign_vehicle_to_route("Bus2", "Route1")
    manager.assign_vehicle_to_route("Bustop1", "Route2")


def test_update_vehicle_location():
    manager = TransportManager()
    bus = Transport("Bustop1", "Bus", (0, 0), "On Time")
    manager.add_vehicle(bus)

    new_location = (1, 1)
    manager.update_vehicle_location("Bustop1", new_location)

    assert bus.get_current_location() == new_location


def test_search_stop():
    manager = TransportManager()
    stop = Stop("stop1", "Stop One", (0, 0))
    route1 = Route("route1", "First Route", [stop])
    manager.add_route(route1)

    found_stop = manager.search_stop("stop1")
    assert found_stop == stop

    found_stop = manager.search_stop("Stop One")
    assert found_stop == stop

    result = manager.search_stop("Nonexistent Stop")
    assert result == "Stop not found"


def test_search_route1():
    manager = TransportManager()
    stop1 = Stop("stop1", "Stop One", (0, 0))
    route1 = Route("route1", "First Route", [stop1])
    manager.add_route(route1)

    found_route = manager.search_route("First Route")
    assert found_route == route1

    found_route = manager.search_route("first route")
    assert found_route == route1

    result = manager.search_route("Route 67")
    assert result == "Route not found"


def test_search_route2():
    manager = TransportManager()
    route1 = Route("Route1", "First Route", [Stop("stop1", "Stop One", (0, 0))])
    route2 = Route("Route2", "Second Route", [Stop("stop2", "Stop Two", (0, 0))])

    manager.add_route(route1)
    manager.add_route(route2)

    thread1 = threading.Thread(target=manager.search_route, args=("First Route",))
    thread2 = threading.Thread(target=manager.search_route, args=("Second Route",))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def test_route_status_updates1():
    manager = TransportManager()
    route = Route("route1", "Route 1", ["Stop1", "Stop2"])
    manager.add_route(route)

    new_status1 = "Delayed"
    new_status2 = "On Time"

    thread1 = threading.Thread(target=route.update_status, args=(new_status1,))
    thread2 = threading.Thread(target=route.update_status, args=(new_status2,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert route.get_status() == new_status2


def test_route_status_updates2():
    manager = initialize_transport_manager_from_files("Vehicle.txt", "Route.txt", "Stops.txt")

    new_status1 = "Delayed"
    new_status2 = "On Time"
    new_status3 = "Early"

    thread1 = threading.Thread(target=manager.routes["R101"].update_status, args=(new_status1,))
    thread2 = threading.Thread(target=manager.routes["R102"].update_status, args=(new_status2,))
    thread3 = threading.Thread(target=manager.routes["R103"].update_status, args=(new_status3,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    assert manager.routes["R101"].get_status() == new_status1
    assert manager.routes["R102"].get_status() == new_status2
    assert manager.routes["R103"].get_status() == new_status3


def test_route_status_updates3():
    manager = initialize_transport_manager_from_files("Vehicle.txt", "Route.txt", "Stops.txt")

    new_status1 = "Delayed"
    new_status2 = "On Time"

    thread1 = threading.Thread(target=manager.routes["R101"].update_status, args=(new_status1,))
    thread2 = threading.Thread(target=manager.routes["R102"].update_status, args=(new_status2,))
    thread3 = threading.Thread(target=manager.routes["R103"].update_status, args=(new_status1,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    assert manager.routes["R101"].get_status() == new_status1
    assert manager.routes["R102"].get_status() == new_status2
    assert manager.routes["R103"].get_status() == new_status1


def test_route_assignment():
    manager = TransportManager()
    route = Route("route1", "Route 1", ["Stop1", "Stop2"])
    manager.add_route(route)
    vehicle = Transport("Vehicle1", "Bus", (0, 0), "On Time")
    manager.add_vehicle(vehicle)

    thread1 = threading.Thread(target=manager.assign_vehicle_to_route, args=("Vehicle1", "route1"))
    thread2 = threading.Thread(target=manager.assign_vehicle_to_route, args=("Vehicle1", "route1"))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert len(route.get_vehicles()) == 2


def test_stop_search():
    manager = TransportManager()
    route1 = Route("Route1", "First Route", [Stop("stop1", "Stop One", (0, 0))])
    route2 = Route("Route2", "Second Route", [Stop("stop2", "Stop Two", (0, 0))])

    manager.add_route(route1)
    manager.add_route(route2)

    thread1 = threading.Thread(target=manager.search_stop, args=("stop1",))
    thread2 = threading.Thread(target=manager.search_stop, args=("stop2",))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert isinstance(manager.search_stop("stop1"), Stop)
    assert isinstance(manager.search_stop("stop2"), Stop)
    assert isinstance(manager.search_route("First Route"), Route)
    assert isinstance(manager.search_route("Second Route"), Route)


def test_vehicle_updates():
    manager = initialize_transport_manager_from_files("Vehicle.txt", "Route.txt", "Stops.txt")

    new_location1 = (40.734502, -74.16476)
    new_location2 = (40.73276, -74.0621)

    thread1 = threading.Thread(target=manager.update_vehicle_location, args=("V101", new_location1))
    thread2 = threading.Thread(target=manager.update_vehicle_location, args=("V102", new_location2))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
