import pyautogui
from line_profiler import LineProfiler, profile
import time
from datetime import datetime
import cv2
import numpy as np
from pynput import mouse
import dxcam
from PIL import Image

# Initialisation des variables
x, y = 0, 0
color = (83, 83, 83)
last_pos = None
camera = dxcam.create(output_color="RGB") 



@profile
def get_line(region):

    global last_pos
    frame = camera.grab(region=region)

    if not isinstance(frame, np.ndarray) :
        return

    screenshot = Image.fromarray(frame)

    #screenshot.show()

    # Obtenir les dimensions de l'image
    width, height = screenshot.size

    pixels = []

    # Afficher la couleur de chaque pixel
    y2 = 0
    for x2 in range(width):
        r, g, b = screenshot.getpixel((x2, y2))
        if (r, g, b) == color :
            pixels.append(x2)#return True
    
    if pixels != [] :
        return True
        pos = x + pixels[-1]
        if pos <= 323 :
            return True
        elif last_pos :
            v = (pos - last_pos[1]) / (int(time.time() * 1000) - last_pos[0])
            print(v)
            last_pos = None
        else :
            last_pos = (int(time.time() * 1000), pos)

    return False

def on_click(x_event, y_event, button, pressed):
    global x
    global y
    if pressed and button == mouse.Button.left :
        print(f'Mouse clicked at ({x_event}, {y_event}) with {(button)}')
        x, y = x_event, y_event
        return False
        

print('Choice point a with a click')

# Collecte des événements jusqu'à ce que l'utilisateur arrête le programme
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

"""
x1, y1 = x, y

print('Choice point b with a click')

# Collecte des événements jusqu'à ce que l'utilisateur arrête le programme
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

x2, y2 = x, y

print(f"Start with zone {x1};{y1}:{x2};{y2}")
"""

region = (x, y, x+117, y+1)

while True :
    try:
        if get_line(region) : 
            pyautogui.press('space')
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' : jump')
    except KeyboardInterrupt:
        print("Fin")
        break
    
