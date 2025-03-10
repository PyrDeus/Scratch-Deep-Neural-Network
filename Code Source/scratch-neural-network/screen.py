###
# screen.py
# Useful view classes

# Opencv values doc: https://docs.opencv.org/4.5.0/d4/dd5/highgui_8hpp.html

from shape import *
from typing import List
from sample import *
from sample import color_classes, shape_classes

from abc import ABC, abstractmethod
import numpy as np
import cv2
import os
import ast

class Canvas(ABC):
    def _createBlankCanvas(self, width, height) -> np.ndarray:
        return np.ones((height, width, 3), dtype="uint8")*255


# Not in RGB, OpenCV uses BGR
color_selection = {
    0: (0, 0, 255),
    1: (0, 255, 0),
    2: (255, 0, 0),
    3: (0, 255, 255),
    4: (255, 255, 0),
    5: (255, 0, 255),
    (0, 0, 255): 0,
    (0, 255, 0): 1,
    (255, 0, 0): 2,
    (0, 255, 255): 3,
    (255, 255, 0): 4,
    (255, 0, 255): 5
}
shape_selection = {
    0: Circle,
    1: Triangle,
    2: Square,
    3: Pentagon,
    4: Hexagon,
    Circle: 0,
    Triangle: 1,
    Square: 2,
    Pentagon: 3,
    Hexagon: 4
}


class Selector(Canvas):
    def __init__(self):
        self.name = f"{id(self)}"
        self.shape = Circle((100,100), 100, color = (0, 0, 255), thickness = -1)
        self.color = (0, 0, 255)
        self.update()

        cv2.imshow(self.name, self.canvas)
        cv2.createTrackbar('color', self.name, 0, 5, self.__color_trackbar)
        cv2.createTrackbar('shape', self.name, 0, 4, self.__shape_trackbar)

    def update(self):
        self.canvas = self._createBlankCanvas(200, 200)
        self.shape.draw(self.canvas)
        cv2.imshow(self.name, self.canvas)

    def __color_trackbar(self, value):
        color = color_selection[value]

        self.color = color
        self.shape.setColor(color)
        self.update()

    def __shape_trackbar(self, value):
        self.shape = shape_selection[value](center=(100,100), radius=100, color=self.color, thickness=-1)
        self.update()

    def setShape(self, sample: Sample2D):
        self.color = sample.getColor()
        self.shape = sample.getShape()(center=(100,100), radius=100, color=self.color, thickness=-1)
        
        cv2.setTrackbarPos('shape', self.name, shape_selection[type(self.shape)])
        cv2.setTrackbarPos('color', self.name, color_selection[self.color])
        self.update()
    # def setShape(self, shape: type[Drawable]):
    #     self.shape = shape(center=(100,100), radius=100, color=self.color, thickness=-1)
    def setColor(self, color: tuple[int, int, int]):
        self.shape.setColor(color)
        self.color = color
        cv2.setTrackbarPos('color', self.name, color_selection[color])
        self.update()

    def getShapeLabel(self) -> str:
        return shape_classes[type(self.shape)]
    def getColorLabel(self) -> str:
        return color_classes[self.color]

class Screen(Canvas):
    def __init__(self, width:int = 640, height:int = 480, name:str = None, selector=False):
        self.width = width
        self.height = height
        self.shapes: List[Shape] = []
        self.canvas = self._createBlankCanvas(width, height)
        if name is None:
            self.name = str(id(self))
        else:
            self.name = name

        self.__drawCanvas()
        if selector == True:
            self.selector = Selector()
            cv2.setMouseCallback(self.name, self.__mouse)

    def __str__(self, view: bool = True, model:bool = True) -> str:
        if view: print(f"- View -\nWidth: {self.width}, Height: {self.height}\n")
        if model: print("\n".join(str(s) for s in self.shapes))

    def setDimensions(self, width: int, height: int):
        self.width = width
        self.height = height
        self.view.setDimensions(width, height)
    
    def getDimensions(self) -> tuple[int, int]:
        return self.width, self.height

    def getName(self) -> str:
        return self.name

    def add(self, shape: Drawable):
        self.shapes.append(shape)

    def extend(self, shapes: List[Drawable]):
        self.shapes.extend(shapes)

    def getDrawn(self) -> List[Drawable]:
        return self.shapes

    def set(self, shapes: List[Drawable]):
        #self.shapes = [] # Needed?
        self.shapes = shapes

    def __drawCanvas(self):
        for s in self.shapes:
            s.draw(self.canvas)
        cv2.imshow(self.name, self.canvas)

    def run(self, update_time=10):
        while True:
            # Get a numpy array to display from the simulation
            self.canvas = self.__drawCanvas()

            cv2.imshow(self.name, self.canvas)
            if self.waitEvent(update_time) < 1:
                break
        cv2.destroyAllWindows() # Garde-fou

    def __save_model(self, filename):
        if os.path.exists(filename):
            i = 1
            f = f"{filename} ({i})"
            while os.path.exists(f):
                i += 1
                f = f"{filename} ({i})"
            filename = f

        with open(filename, 'x') as file:
            for s in self.shapes:
                file.write(f"{dict(s)}\n")
    
    def __load_model(self, filename):
        self.shapes: List[Shape] = []
        with open(filename, 'r') as file:
            for line in file:
                sample_dict = ast.literal_eval(line)
                self.add(Sample2D(sample_dict['position'], 
                sample_dict['shape'], 
                sample_dict['color']))
        self.canvas = self._createBlankCanvas(self.width, self.height)
        self.__to_front()

    def __to_front(self, selector=True):
        cv2.setWindowProperty(self.name, cv2.WND_PROP_TOPMOST, 1)
        if selector: cv2.setWindowProperty(self.selector.name, cv2.WND_PROP_TOPMOST, 1)

    def waitEvent(self, time=30, verbose=False):
        # 1: Nothing
        # 0: Window closed
        # < 0: All events that should terminate the running
        keys = cv2.waitKey(time)
        if cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1:        
            return 0
        
        screen.update()
        if verbose and keys != -1: print(f"keys = {keys}")
        if keys == 27: # Escape key
            return 0
        elif keys == ord('s'):
            self.__save_model("levels\creation_model")
            return 1
        elif keys == ord('l'):
            levels = dict(enumerate(os.listdir("levels")))
            
            for key, value in levels.items():
                print(f"{key}:  {value}")
            index = int(input("Which level to choose?\n"))
            while index not in levels.keys():
                for key, value in levels.items():
                    print(f"{key}:  {value}")
                    
                index = int(input(f"\"{index}\" is an unexpected value, which level to choose?\n"))

            self.__load_model(f"levels\{levels[index]}")
            return 1
        elif keys == 32: #spacebar
            return 2
        return 1

    def waitKey(self, verbose=False):
        # key = 32 is the spacebar by default
        while True:
            match self.waitEvent(time = 100, verbose=verbose):
                case 1:
                    continue
                case 2:
                    return 1
                case 0:
                    return 0
                case _:
                    return "unexpected"
        return 1

    def show(self):
        cv2.imshow(self.name, self.canvas)

    def update(self):
        self.__drawCanvas()

    def destroyWindow(self):
        self.update()
        cv2.destroyWindow(self.name)

    def __closestShape(self, x, y):
        if len(self.shapes) == 0:
            return None
        closest_shape = self.shapes[0]
        closest_v = np.abs(closest_shape.x - x) + np.abs(closest_shape.y - y)
        for s in self.shapes[1:]:
            v = np.abs(s.x - x) + np.abs(s.y - y)
            if v < closest_v:
                closest_shape = s
                closest_v = v
        return closest_shape
    
    def removeShape(self, shape_id: int):
        i = None
        for i, shape in enumerate(self.shapes):
            if shape_id == id(shape):
                break
        self.shapes.pop(i)
        self.canvas = self._createBlankCanvas(self.width, self.height)

    def removeShape(self, shape: Drawable):
        self.shapes.remove(shape)
        self.canvas = self._createBlankCanvas(self.width, self.height)

    def detectColor(self, x, y):
        return np.any(self.canvas[y, x, :] != [255, 255, 255])

    def __mouse(self, event, x, y, flags, param):
        # print(x, y, event, flags, param)
        if event == 1:
            # print(f"Left-button pressed on {(x,y)}")
            if self.detectColor(x, y):
                self.removeShape(self.__closestShape(x, y))
                print("Shape removed")
            else:
                self.add(Sample2D((x,y), 
                self.selector.getShapeLabel(), 
                self.selector.getColorLabel()))
                print("Shape added")
            
        elif event == 2:
            # print(f"Right-button pressed on {(x,y)}")
            if self.detectColor(x,y):
                selected_shape = self.__closestShape(x, y)
                # print(selected_shape)
                self.selector.setShape(selected_shape)
                print(f"Shape selected:\n{selected_shape}")
            else:
                print("No shape selected")
        elif event == 3:
            pt = np.random.randint([0, 0], [w, h]) ## Avoid collision with other shape ?
            created_shape = Sample2D(pt, random_shape_label(), random_color_label())
            self.add(created_shape)
            self.selector.setShape(created_shape)
            print("Random shape created")


        
        # elif event == 7:
        #     print(f"Double Left-button clicked on {(x,y)}")

if __name__ == "__main__":
    import cv2
    from utils import random_color_label, random_shape_label

    # w, h = extractMonitorDimensions()
    w, h = 640, 480
    screen = Screen(w, h, name="image", selector=True)
    screen.show()

    while True:

        criteria = screen.waitKey(verbose=False)
        if criteria == 0:
            break

        pt = np.random.randint([0, 0], [w, h])
        screen.add(Sample2D(pt, random_shape_label(), random_color_label()))
        
        screen.update()
    screen.destroyWindow() # Garde-fou




