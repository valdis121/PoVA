import time
import os
from geopy.distance import geodesic
import folium
from selenium import webdriver
import math
import cv2


def calculate_map_dimensions(center, zoom_level, aspect_ratio=1.0):
    earth_radius = 6371.0

    map_length = math.pow(2, 21 - zoom_level) * 256 / earth_radius
    map_width = map_length * aspect_ratio
    map_height = map_length

    return map_width, map_height

def calculate_distance(left, right, height):
    distance_meters = geodesic(left, right).meters
    distance_kilometers = distance_meters / 1000
    kilometers_per_pixel = distance_kilometers / height
    return kilometers_per_pixel

def save_map_as_html(mymap, html_file):
    mymap.save(html_file)

def open_map_in_browser(html_file):
    current_dir = os.getcwd()
    browser = webdriver.Chrome()
    browser.get('file://' + os.path.join(current_dir, html_file))
    time.sleep(5)
    browser.save_screenshot('map.png')
    browser.quit()

def get_map_edges(center, zoom_level, width, height):
    center_lat, center_lng = center

    lat_distance = height / 2
    lng_distance = width / 2

    top_left = (center_lat + lat_distance, center_lng - lng_distance)
    bottom_right = (center_lat - lat_distance, center_lng + lng_distance)

    top_center = (center_lat + lat_distance, center_lng)
    bottom_center = (center_lat - lat_distance, center_lng)

    return top_left, bottom_right, top_center, bottom_center

def main():
    middle = (51.041777, 13.735755)
    zoom = 18

    # take small radius around middle point
    left = (middle[0] - 0.0011, middle[1])
    right = (middle[0] + 0.00109999999, middle[1])


    mymap = folium.Map(location=middle, zoom_start=zoom, control_scale=True)
    satellite_layer = folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=True,
        control=True
    )
    satellite_layer.add_to(mymap)

    html_file = 'map_folium.html'
    save_map_as_html(mymap, html_file)

    open_map_in_browser(html_file)

    image = cv2.imread("map.png")
    height = image.shape[0]
    speed = calculate_distance(left, right, height)
    print("Speed {}km/pix".format(speed))
if __name__ == "__main__":
    main()


