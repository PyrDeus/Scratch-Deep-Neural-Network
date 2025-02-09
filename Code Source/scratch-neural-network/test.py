#!/usr/local/bin/python3

from screen import *

import cv2


w, h = 640, 480
screen = Screen(w,h)
screen.show()


while True:
    cv2.waitKey(300)
    if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:        
        break
    
    # screen.erase()

    pt_1 = np.random.randint([0, 0], [w, h])
    pt_2 = np.random.randint([0, 0], [w, h])
    
    color = np.random.uniform([0, 0, 0], [255, 255, 255])
    thickness = np.random.randint(-1, 5)

    screen.addShape(Rectangle(pt_1, pt_2, color, thickness))
    
    screen.update()
    

cv2.destroyAllWindows() # Garde-fou