###
# screen.py
# Useful view classes


from shape import *
from typing import List

import numpy as np
import cv2

class Screen:
  
    def __init__(self, width:int = 640, height:int = 480):
        self.width = width
        self.height = height
        self.shapes: List[Shape] = []
        self.canvas = self.__createBlankCanvas(width, height)

    def __str__(self, view: bool = True, model:bool = True) -> str:
        if view: print(f"- View -\nWidth: {self.width}, Height: {self.height}\n")
        if model: print("\n".join(str(s) for s in self.shapes))

    def __createBlankCanvas(self, width, height) -> np.ndarray:
        return np.ones((height, width, 3), dtype="uint8")

    def setDimensions(width: int, height: int):
        self.width = width
        self.height = height
        self.view.setDimensions(width, height)
    
    def getDimensions() -> tuple[int, int]:
        return self.width, self.height

    def addShape(self, shape: Shape):
        self.shapes.append(shape)

    def addShapes(self, shapes: List[Shape]):
        self.shapes.extend(shapes)

    def getShapes(self) -> List[Shape]:
        return self.shapes

    def setShapes(self, shapes: List[Shape]):
        #self.shapes = [] # Needed?
        self.shapes = shapes 

    def __drawCanvas(self):
        for s in self.shapes:
            s.draw(self.canvas)
        cv2.imshow("image", self.canvas)

    def run(self, framerate=10, label_image:str = "image"):
        while True:
            # Get a numpy array to display from the simulation
            self.canvas = self.__drawCanvas()

            cv2.imshow(label_image, self.canvas)
            cv2.waitKey(framerate)
            if cv2.getWindowProperty(label_image, cv2.WND_PROP_VISIBLE) < 1:        
                break
            cv2.destroyAllWindows() # Garde-fou

    def show(self, label_image:str = "image"):
        cv2.imshow(label_image, self.canvas)

    def update(self):
        # Draw all from scratch but could remember which shape was modified and if it should redraw from scratch
        self.__drawCanvas()
    
    def erase(self):
        self.shapes: List[Shape] = []
        self.canvas = self.__createBlankCanvas(self.width, self.height)



if __name__ == "__main__":
    import cv2

    # w, h = extractMonitorDimensions()
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