from geopy.distance import geodesic
import folium


# Set the coordinates of the bottom left corner
bottom_left = (37.773972, -122.430673)

# Set the dimensions and scale
width = 800  # width in pixels
height = 600  # height in pixels
zoom = 15  # zoom level (larger value means closer)

# Set the coordinates of the top right corner
top_right = (bottom_left[0] + height * 360 / (2 ** zoom), bottom_left[1] + width * 360 / (2 ** zoom))

# Calculate the distance between two points (in meters)
distance_meters = geodesic(bottom_left, top_right).meters

# Convert the distance to kilometers
distance_kilometers = distance_meters / 1000

# Calculate kilometers per pixel
kilometers_per_pixel = distance_kilometers / width

print(f'Kilometers per pixel: {kilometers_per_pixel:.6f} km/pixel')

# Create a folium map object
mymap = folium.Map(location=bottom_left, zoom_start=zoom, control_scale=True)

# Save the map as an HTML file
html_file = 'map_folium.html'
mymap.save(html_file)


