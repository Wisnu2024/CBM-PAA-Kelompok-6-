import numpy as np
from PIL import Image
import random
import tkinter as tk


map_width, map_height = 150, 150
cell_size = 32  


city_map = np.zeros((map_height * cell_size, map_width * cell_size, 3), dtype=np.uint8)
occupied_map = np.zeros((map_height, map_width), dtype=bool)  


def place_building(image_path, top_left, size):
    building = Image.open(image_path).convert('RGB')  
    building = building.resize((size[0]*cell_size, size[1]*cell_size), Image.Resampling.LANCZOS)
    y_start = top_left[1]*cell_size
    y_end = y_start + size[1]*cell_size
    x_start = top_left[0]*cell_size
    x_end = x_start + size[0]*cell_size

    
    if not occupied_map[top_left[1]:top_left[1]+size[1], top_left[0]:top_left[0]+size[0]].any():
        if x_end <= map_width * cell_size and y_end <= map_height * cell_size:
            city_map[y_start:y_end, x_start:x_end] = np.array(building)
            occupied_map[top_left[1]:top_left[1]+size[1], top_left[0]:top_left[0]+size[0]] = True


def place_road(image_path, start, end):
    road = Image.open(image_path).convert('RGB')
    road = road.resize((cell_size, cell_size), Image.Resampling.LANCZOS)

    if start[0] == end[0]:  # Jalan vertikal
        for y in range(start[1], end[1]+1):
            if not occupied_map[y, start[0]]:
                city_map[y*cell_size:(y+1)*cell_size, start[0]*cell_size:(start[0]+1)*cell_size] = np.array(road)
                occupied_map[y, start[0]] = True
    else:  # Jalan horizontal
        for x in range(start[0], end[0]+1):
            if not occupied_map[start[1], x]:
                city_map[start[1]*cell_size:(start[1]+1)*cell_size, x*cell_size:(x+1)*cell_size] = np.array(road)
                occupied_map[start[1], x] = True


def redesign_city():
    global city_map, occupied_map
    city_map.fill(0)  
    occupied_map.fill(False)  

    
    for i in range(10, 140, 10):
        if random.choice([True, False]):
            place_road("C:/Users/mwisn/OneDrive/Documents/SEMESTER 4/PAA/new/Road.png", (i, 0), (i, map_height-1))
        else:
            place_road("C:/Users/mwisn/OneDrive/Documents/SEMESTER 4/PAA/new/Road.png", (0, i), (map_width-1, i))

    
    for _ in range(1):
        top_left = (random.randint(0, map_width-10), random.randint(0, map_height-5))
        place_building("C:/Users/mwisn/OneDrive/Documents/SEMESTER 4/PAA/new/Big Building.png", top_left, (10, 5))
    for _ in range(4):
        top_left = (random.randint(0, map_width-5), random.randint(0, map_height-3))
        place_building("C:/Users/mwisn/OneDrive/Documents/SEMESTER 4/PAA/new/Medium Building.png", top_left, (5, 3))
    for _ in range(10):
        top_left = (random.randint(0, map_width-2), random.randint(0, map_height-2))
        place_building("C:/Users/mwisn/OneDrive/Documents/SEMESTER 4/PAA/new/Small Building.png", top_left, (2, 2))
    for _ in range(10):
        top_left = (random.randint(0, map_width-1), random.randint(0, map_height-2))
        place_building("C:/Users/mwisn/OneDrive/Documents/SEMESTER 4/PAA/new/House.png", top_left, (1, 2))


def update_map():
    redesign_city()
    final_map = Image.fromarray(city_map)
    final_map.save("city_map.png")
    final_map.show()


root = tk.Tk()
root.title("City Map Generator")


button = tk.Button(root, text="Redesign Map", command=update_map)
button.pack(side=tk.BOTTOM)

root.mainloop()