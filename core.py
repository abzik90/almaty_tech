from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import requests
import os
BING_MAPS_API = os.environ.get("BING_MAPS_API_KEY")
print(BING_MAPS_API)

def get_distance(coords_1, coords_2):
    global BING_MAPS_API_KEY
    url = f'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={coords_1}&destinations={coords_2}&travelMode=driving&key={BING_MAPS_API}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'resourceSets' in data and len(data['resourceSets']) > 0:
            resources = data['resourceSets'][0]['resources']
            if len(resources) > 0:
                return resources[0]['results'][0]['travelDistance']
    print("Unable to get the distance")
    print(url)

    return float('inf')


def create_data_model(locations):
    distance_matrix = []
    for i in range(len(locations)):
        row = []
        for j in range(len(locations)):
            if i == j:
                row.append(0)
            else:
                coords1 = locations[i]['coordinate']
                coords2 = locations[j]['coordinate']
                distance = get_distance(", ".join(str(item) for item in coords1), ", ".join(str(item) for item in coords2))
                row.append(distance)
        distance_matrix.append(row)

    data = {
        'distance_matrix': distance_matrix,
        'num_vehicles': 1,
        'depot': 0
    }

    return data
def solve_tsp(data):
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,
        10000,
        True,
        dimension_name)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        return solution, routing, manager
    else:
        print('No solution found!')
        return None

def print_solution(solution, routing, manager, data, locations):
    total_distance = 0
    index = routing.Start(0)
    plan_output = 'Route for Vehicle 0:\n'
    coord_output = []
    route_distance = 0
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        plan_output += f'{locations[node_index]["name"]} -> '
        coord_output.append(locations[node_index]["coordinate"])
        next_node_index = manager.IndexToNode(solution.Value(routing.NextVar(index)))
        route_distance += data['distance_matrix'][node_index][next_node_index]
        index = solution.Value(routing.NextVar(index))

    plan_output += f'{locations[manager.IndexToNode(index)]["name"]}'
    route_distance += data['distance_matrix'][manager.IndexToNode(index)][0]
    route_distance = float(route_distance) * 1.61
    plan_output += f' (Distance: {route_distance:.2f} km)\n'
    total_distance += route_distance

    print(plan_output)
    print('Total distance:', total_distance, 'km')
  
    return plan_output, total_distance, coord_output

def solve_for_coords(coord_list):
    locations = [{'name': f'Location {i+1}','coordinate': coordinate} for i, coordinate in enumerate(coord_list)]
    data = create_data_model(locations)

    solution, routing, manager = solve_tsp(data)
    if solution:
        _, _, coord_output = print_solution(solution, routing, manager, data, locations)
        return coord_output
    else:
        print('No solution found!')
        return []