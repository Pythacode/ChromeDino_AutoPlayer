import cv2 as cv
import numpy as np
from PIL import ImageGrab
import pyautogui
from datetime import datetime
import asyncio
import time

speed = 0
last_pos = 0
last_time = int(time.time())

region = None

dino_ref = cv.imread("dino.png")

if dino_ref is None:
    print("ERREUR : Impossible de charger l'image du dino")
    exit(1)

if len(dino_ref.shape) > 2 and dino_ref.shape[2] > 1:
    dino_ref = cv.cvtColor(dino_ref, cv.COLOR_BGR2GRAY)

cactus_ref = cv.imread("cactus.png")

if cactus_ref is None:
    print("ERREUR : Impossible de charger l'image du cactus")
    exit(1)

if len(cactus_ref.shape) > 2 and cactus_ref.shape[2] > 1:
    cactus_ref = cv.cvtColor(cactus_ref, cv.COLOR_BGR2GRAY)

async def jump(time) :
    await asyncio.sleep(time)
    pyautogui.press('space')


def diagnose_template_matching(obg):

    global region
    global speed
    global last_pos

    # Capture d'écran
    screenshot = np.array(ImageGrab.grab(bbox=region))
    
    # Convertir les images si nécessaire
    try:
        # Convertir la capture d'écran en niveaux de gris
        screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)

        # Effectuer la correspondance de modèle
        result = cv.matchTemplate(screenshot_gray, obg, cv.TM_CCOEFF_NORMED)
        
        # Trouver la valeur maximale de correspondance
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        
        #print(f"Meilleur score de correspondance : {max_val}  |", end="")
        #print('\b' * 1000, end='', flush=True)
        

        if not region :
            region = (max_loc[0]+60, max_loc[1], max_loc[0] + 700, max_loc[1] + 50)
        
        """top_left = (max_loc[0]+60, max_loc[1])
        bottom_right = (top_left[0] + 100, top_left[1] + 50)
        cv.rectangle(screenshot_gray, top_left, bottom_right, color=(0, 255, 0), thickness=2)

        # Afficher l'image avec le rectangle
        cv.imshow('Image avec template matching', screenshot_gray)
        cv.waitKey(0)
        cv.destroyAllWindows()"""

        if obg is cactus_ref : 
            if max_val > 0.2 :

                speed = (last_pos - max_loc[0])/(time.time()/last_time)
                last_pos = max_loc[0] 

                #print(f"Speed : {speed} p/s | Distance : {max_loc[0]} p |", end="")
                #print('\b' * 1000, end='', flush=True)

                if speed != 0 and max_loc[0]-50/speed > 0 :
                    return max_loc[0]/speed
                else : return False
            
            else : return False

        else : return max_val > 0.8
        
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return False

if not diagnose_template_matching(dino_ref) :
    print("Dino not found")
    exit(2)

async def main() :
    print("Start")
    n = 0
    while True :
        try:
            result = diagnose_template_matching(cactus_ref)
            print(result, speed)
            if result :
                asyncio.create_task(jump(result))
        except KeyboardInterrupt:
            print("Fin")
            break
        n += 1

asyncio.run(main())