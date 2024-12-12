import requests
import folium
import polyline

# Base OSRM server URL
osrm_base_url = "http://localhost:5001"

# Start and end coordinates
start_coord = (26.1445, 91.7362)  # Latitude, Longitude
end_coord = (25.5788, 91.8807)

# OSRM API route request
route_url = f"{osrm_base_url}/route/v1/driving/{start_coord[1]},{start_coord[0]};{end_coord[1]},{end_coord[0]}?overview=full&geometries=polyline"
response = requests.get(route_url)
route_data = response.json()

# Extract route geometry and decode polyline
route_geometry = route_data['routes'][0]['geometry']
decoded_route = polyline.decode(route_geometry)  # List of (lat, lon) points

# Create a map centered at the start location
route_map = folium.Map(location=start_coord, zoom_start=10)

# Add the route to the map
folium.PolyLine(decoded_route, color="blue", weight=2.5, opacity=0.8).add_to(route_map)

# Add markers for start and end points
folium.Marker(location=start_coord, popup="Start", icon=folium.Icon(color="green")).add_to(route_map)
folium.Marker(location=end_coord, popup="End", icon=folium.Icon(color="red")).add_to(route_map)

# Save map to an HTML file and display
route_map.save("route_map.html")
print("Map saved as route_map.html")