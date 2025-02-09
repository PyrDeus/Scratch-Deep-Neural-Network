###
# shape.py
# Contains shapes and useful classes to use on the canvas of the Screen class (screen.py) 


from utils import *

import cv2
from abc import ABC, abstractmethod

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
    def __init__(self, point_1: tuple[int, int], point_2: tuple[int, int], color: Color = Color.BLACK, thickness:int = 3):
        super().__init__(color, thickness)
        self.point_1 = point_1
        self.point_2 = point_2

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Line\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color}"

    def draw(self, canvas):
        cv2.line(canvas, self.point_1, self.point_2, self.color, self.thickness)

class Circle(Shape):
    def __init__(self, center: tuple[int, int], radius: int, color: Color = Color.BLACK, thickness:int = 3):
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
        return f"Class Shape\nSubclass Circle\nCenter: {self.center}\nRadius: {self.radius}\nColor: {self.color}"

    def draw(self, canvas):
        # negative value for thickness means fill
        cv2.circle(canvas, self.center, self.radius, self.color, self.thickness)


class Rectangle(Shape):
    def __init__(self, point_1: tuple[int, int], point_2: tuple[int, int], color: Color = Color.BLACK, thickness:int = 3):
        super().__init__(color, thickness)
        self.point_1 = point_1
        self.point_2 = point_2

    def getPt1(self) -> int:
        return self.point_1

    def setPt1(self, point_1: int):
        self.point_1 = point_1

    def getPt2(self) -> int:
        return self.point_2

    def setPt2(self, point_2: int):
        self.point_2 = point_2

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Rectangle\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color}"

    def draw(self, canvas):
        # negative value for thickness means fill
        cv2.rectangle(canvas, self.point_1, self.point_2, self.color, self.thickness)
        # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        # pts = pts.reshape((-1,1,2))
        # cv.polylines(img,[pts],True,(0,255,255))


