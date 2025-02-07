#!/usr/local/bin/python3
import numpy as np
import cv2
from typing import List, Tuple
from abc import ABC, abstractmethod
from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GRAY = (128, 128, 128)
    LIME = (0, 255, 0)
    OLIVE = (128, 128, 0)
    NAVY = (0, 0, 128)
    TEAL = (0, 128, 128)
    MAROON = (128, 0, 0)
    SILVER = (192, 192, 192)
    GOLD = (255, 215, 0)

class Shape(ABC):
    def __init__(self, color:Color = Color.BLACK, thickness:int = 3):
        self.color = color
        self.thickness = thickness
    
    def __str__(self) -> str:
        return f"Class Shape\nSubclass None\nPosition: {self.position}"
    
    @abstractmethod
    def draw():
        pass

    def setColor(self, color:Color):
        self.color = color
    def getColor(self) -> Color:
        return self.color


class Line(Shape):
    def __init__(self, point_1: Tuple[int, int], point_2: Tuple[int, int], color: Color = Color.BLACK, thickness:int = 3):
        super().__init__(color, thickness)
        self.point_1 = point_1
        self.point_2 = point_2

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Line\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color.name}"

    def draw(self, canvas):
        cv2.line(canvas, self.point_1, self.point_2, self.color, self.thickness)

class Circle(Shape):
    def __init__(self, center: Tuple[int, int], radius: int, color: Color = Color.BLACK, thickness:int = 3):
        super().__init__(color, thickness)
        self.center = center
        self.radius = radius

    def getCenter(self) -> int:
        return self.center

    def setCenter(self, center: tuple[int, int]):
        self.center = center

    def getRadius(self) -> int:
        return self.radius

    def setRadius(self, radius: int):
        self.radius = radius

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Circle\nCenter: {self.center}\nRadius: {self.radius}\nColor: {self.color.name}"

    def draw(self, canvas):
        # negative value for thickness means fill
        cv2.circle(canvas, self.center, self.radius, self.color, self.thickness)


class Rectangle(Shape):
    def __init__(self, point_1: Tuple[int, int], point_2: Tuple[int, int], color: Color = Color.BLACK, thickness:int = 3):
        super().__init__(color, thickness)
        self.point_1 = point_1
        self.point_2 = point_2

    def getPt1(self) -> int:
        return self.point_1

    def setPt1(self, point_1: int):
        self.point_1 = point_1

    def getP2(self) -> int:
        return self.point_2

    def setPt1(self, point_2: int):
        self.point_2 = point_2

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Rectangle\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color.name}"

    def draw(self, canvas):
        # negative value for thickness means fill
        cv2.rectangle(canvas, self.point_1, self.point_2, self.color, self.thickness)
        # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        # pts = pts.reshape((-1,1,2))
        # cv.polylines(img,[pts],True,(0,255,255))

class Screen:
  
    def __init__(self, width:int = 640, height:int = 480):
        self.width = width
        self.height = height
        self.shapes: List[Shape] = []
        self.canvas = np.ones((width, height, 3), dtype="uint8")

    def __str__(self, view: bool = True, model:bool = True) -> str:
        if view: print(f"- View -\nWidth: {self.width}, Height: {self.height}\n")
        if model: print("\n".join(str(s) for s in self.shapes))

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

    def __drawCanvas(self, erase=True):
        if erase:
            self.canvas = np.ones((self.width, self.height, 3), dtype="uint8")

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

    def update(self, erase=True):
        # Draw all from scratch but could remember which shape was modified and if it should redraw from scratch
        self.__drawCanvas(erase=erase)
    


w, h = 640, 480
screen = Screen(w,h)
screen.show()


while True:
    cv2.waitKey(100)
    if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:        
        break
    
    pt_1 = np.random.randint([0, 0], [h, w])
    pt_2 = np.random.randint([0, 0], [h, w])
    
    color = np.random.uniform([0, 0, 0], [255, 255, 255])
    thickness = np.random.randint(-1, 5)

    screen.addShape(Rectangle(pt_1, pt_2, color, thickness))
    screen.update(erase=False)
    

cv2.destroyAllWindows() # Garde-fou