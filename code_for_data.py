# import csv
# from random import uniform
# from math import radians, sin, cos, sqrt, atan2
#
# # Function to generate coordinates around a given center
# def generate_coordinates(n, center_lat, center_lon, radius):
#     locations = []
#     for i in range(1, n + 1):
#         lat = uniform(center_lat - radius, center_lat + radius)
#         lon = uniform(center_lon - radius, center_lon + radius)
#         locations.append({"id": i, "latitude": round(lat, 6), "longitude": round(lon, 6)})
#     return locations
#
# # Haversine formula to calculate distances between two coordinates
# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371  # Radius of Earth in kilometers
#     dlat = radians(lat2 - lat1)
#     dlon = radians(lon2 - lon1)
#     a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#     return R * c
#
# # Generate real-world coordinates for warehouses and destinations
# center_lat, center_lon = 34.73483, 135.43452  # Given coordinate
# warehouse_radius = 0.5  # Radius in degrees for warehouses
# destination_radius = 1.0  # Radius in degrees for destinations
#
# # Generate data
# warehouses = generate_coordinates(1000, center_lat, center_lon, warehouse_radius)  # 2 warehouses
# destinations = generate_coordinates(2000, center_lat, center_lon, destination_radius)  # 4 destinations
#
# # Calculate all paths (distances between points)
# def calculate_paths(warehouses, destinations):
#     paths = []
#
#     # Distances between warehouses (avoid duplicate paths)
#     for i, warehouse1 in enumerate(warehouses):
#         for j, warehouse2 in enumerate(warehouses):
#             if i < j:  # Ensure no duplicate paths
#                 distance = haversine(
#                     warehouse1["latitude"], warehouse1["longitude"],
#                     warehouse2["latitude"], warehouse2["longitude"]
#                 )
#                 cost = round(distance * 5, 2)  # Example cost formula: cost = 5 * distance
#                 paths.append({
#                     "start_id": warehouse1["id"],
#                     "start_type": "Warehouse",
#                     "start_latitude": warehouse1["latitude"],
#                     "start_longitude": warehouse1["longitude"],
#                     "end_id": warehouse2["id"],
#                     "end_type": "Warehouse",
#                     "end_latitude": warehouse2["latitude"],
#                     "end_longitude": warehouse2["longitude"],
#                     "distance_km": round(distance, 2),
#                     "cost": cost
#                 })
#
#     # Distances between warehouses and destinations
#     for warehouse in warehouses:
#         for destination in destinations:
#             distance = haversine(
#                 warehouse["latitude"], warehouse["longitude"],
#                 destination["latitude"], destination["longitude"]
#             )
#             cost = round(distance * 5, 2)  # Example cost formula: cost = 5 * distance
#             paths.append({
#                 "start_id": warehouse["id"],
#                 "start_type": "Warehouse",
#                 "start_latitude": warehouse["latitude"],
#                 "start_longitude": warehouse["longitude"],
#                 "end_id": destination["id"],
#                 "end_type": "Destination",
#                 "end_latitude": destination["latitude"],
#                 "end_longitude": destination["longitude"],
#                 "distance_km": round(distance, 2),
#                 "cost": cost
#             })
#
#     # Distances between destinations (avoid duplicate paths)
#     for i, destination1 in enumerate(destinations):
#         for j, destination2 in enumerate(destinations):
#             if i < j:  # Ensure no duplicate paths
#                 distance = haversine(
#                     destination1["latitude"], destination1["longitude"],
#                     destination2["latitude"], destination2["longitude"]
#                 )
#                 cost = round(distance * 5, 2)  # Example cost formula: cost = 5 * distance
#                 paths.append({
#                     "start_id": destination1["id"],
#                     "start_type": "Destination",
#                     "start_latitude": destination1["latitude"],
#                     "start_longitude": destination1["longitude"],
#                     "end_id": destination2["id"],
#                     "end_type": "Destination",
#                     "end_latitude": destination2["latitude"],
#                     "end_longitude": destination2["longitude"],
#                     "distance_km": round(distance, 2),
#                     "cost": cost
#                 })
#
#     return paths
#
# # Generate paths
# paths = calculate_paths(warehouses, destinations)
#
# # Save data to CSV
# def save_to_csv(filename, data, fieldnames):
#     with open(filename, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(data)
#
# # Save warehouses, destinations, and paths
# save_to_csv("warehouses.csv", warehouses, ["id", "latitude", "longitude"])
# save_to_csv("destinations.csv", destinations, ["id", "latitude", "longitude"])
# save_to_csv("paths_table.csv", paths, [
#     "start_id", "start_type", "start_latitude", "start_longitude",
#     "end_id", "end_type", "end_latitude", "end_longitude",
#     "distance_km", "cost"
# ])
#
# print("Files generated: warehouses.csv, destinations.csv, paths_table.csv")


import csv
from random import uniform
from math import radians, sin, cos, sqrt, atan2
import pandas as pd

# Function to generate coordinates around a given center
def generate_coordinates(n, center_lat, center_lon, radius):
    locations = []
    for i in range(1, n + 1):
        lat = uniform(center_lat - radius, center_lat + radius)
        lon = uniform(center_lon - radius, center_lon + radius)
        locations.append({"id": i, "latitude": round(lat, 6), "longitude": round(lon, 6)})
    return locations

# Haversine formula to calculate distances between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Generate real-world coordinates for warehouses and destinations
center_lat, center_lon = 34.73483, 135.43452  # Given coordinate
warehouse_radius = 0.5  # Radius in degrees for warehouses
destination_radius = 1.0  # Radius in degrees for destinations

# Generate data
warehouses = generate_coordinates(100, center_lat, center_lon, warehouse_radius)  # 2 warehouses
destinations = generate_coordinates(200, center_lat, center_lon, destination_radius)  # 4 destinations

# Generate matrices for distance and cost
def generate_matrices(warehouses, destinations):
    # Initialize matrices
    destination_vs_destination = {}
    warehouse_vs_warehouse = {}
    warehouse_vs_destination = {}

    # Destination vs Destination matrix
    for dest1 in destinations:
        destination_vs_destination[dest1["id"]] = {}
        for dest2 in destinations:
            if dest1["id"] != dest2["id"]:
                distance = haversine(dest1["latitude"], dest1["longitude"],
                                     dest2["latitude"], dest2["longitude"])
                cost = round(distance * 5, 2)
                destination_vs_destination[dest1["id"]][dest2["id"]] = (round(distance, 2), cost)

    # Warehouse vs Warehouse matrix
    for wh1 in warehouses:
        warehouse_vs_warehouse[wh1["id"]] = {}
        for wh2 in warehouses:
            if wh1["id"] != wh2["id"]:
                distance = haversine(wh1["latitude"], wh1["longitude"],
                                     wh2["latitude"], wh2["longitude"])
                cost = round(distance * 5, 2)
                warehouse_vs_warehouse[wh1["id"]][wh2["id"]] = (round(distance, 2), cost)

    # Warehouse vs Destination matrix
    for wh in warehouses:
        warehouse_vs_destination[wh["id"]] = {}
        for dest in destinations:
            distance = haversine(wh["latitude"], wh["longitude"],
                                 dest["latitude"], dest["longitude"])
            cost = round(distance * 5, 2)
            warehouse_vs_destination[wh["id"]][dest["id"]] = (round(distance, 2), cost)

    return destination_vs_destination, warehouse_vs_warehouse, warehouse_vs_destination

# Generate matrices
destination_vs_destination, warehouse_vs_warehouse, warehouse_vs_destination = generate_matrices(warehouses, destinations)

# Convert matrices to CSV
def save_matrix_to_csv(matrix, filename, row_label, col_label):
    df = pd.DataFrame.from_dict(matrix, orient="index")
    df.index.name = row_label
    df.columns.name = col_label
    df.to_csv(filename)

# Save matrices to CSV files
save_matrix_to_csv(destination_vs_destination, "destination_vs_destination.csv", "Destination", "Destination")
save_matrix_to_csv(warehouse_vs_warehouse, "warehouse_vs_warehouse.csv", "Warehouse", "Warehouse")
save_matrix_to_csv(warehouse_vs_destination, "warehouse_vs_destination.csv", "Warehouse", "Destination")

print("Files generated: destination_vs_destination.csv, warehouse_vs_warehouse.csv, warehouse_vs_destination.csv")
