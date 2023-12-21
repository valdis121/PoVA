import time
import os
from geopy.distance import geodesic
import folium
from selenium import webdriver

def calculate_distance(bottom_left, top_right, width):
    distance_meters = geodesic(bottom_left, top_right).meters
    distance_kilometers = distance_meters / 1000
    kilometers_per_pixel = distance_kilometers / width
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

def main():
    middle = (51.041777, 13.735755)
    width = 1280
    height = 900
    zoom = 18
    # take small radius around middle point
    bottom_left = (middle[0] - 0.0001, middle[1] - 0.0001)
    top_right = (middle[0] + 0.0001, middle[1] + 0.0001)

    kilometers_per_pixel = calculate_distance(bottom_left, top_right, width)
    print(f'Kilometers per pixel: {kilometers_per_pixel:.6f} km/pixel')

    mymap = folium.Map(location=bottom_left, zoom_start=zoom, control_scale=True)
    html_file = 'map_folium.html'
    save_map_as_html(mymap, html_file)
    open_map_in_browser(html_file)

if __name__ == "__main__":
    main()


