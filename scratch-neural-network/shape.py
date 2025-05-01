###
# shape.py
# Contains shapes and useful classes to use on the canvas of the Screen class (window.py)
import copy

from utils import Color

import cv2
from abc import ABC, abstractmethod
import numpy as np
import random


class Drawable(ABC):
    @abstractmethod
    def draw(self, window):
        pass

class Shape(Drawable):
    def __init__(self, position:tuple[int, int], color:Color = Color.BLACK.value, thickness:int = 3):
        self.position = position

        self.color = color
        self.thickness = thickness

    def __str__(self) -> str:
        pass

    def __iter__(self):
        for key, value in self.__dict__:
            yield key, value

    def draw(self, window):
        pass

    def getColor(self) -> tuple[int, int, int]:
        return self.color
    def setColor(self, color:tuple[int, int, int]):
        self.color = color

    def getThickness(self) -> int:
        return self.thickness
    def setThickness(self, thickness: int):
        self.thickness = thickness

    def getPosition(self) -> tuple[int, int]:
        return self.position
    def setPosition(self, position: tuple[int, int]):
        self.position = position

    def getShapeType(self) -> type:
        return type(self)

    def toDict(self) -> dict:
        return {"shape": self.getShapeType(), "color": self.getColor(), "position": self.getPosition(), "thickness": self.getThickness()}

    def copy(self):
        return copy.deepcopy(self)

    def clone(self, **params):
        cloned_version = self.copy()
        for parameter, value in params['diff_params'].items():
            setattr(cloned_version, parameter, value)
        return cloned_version

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]


class Circle(Shape):
    def __init__(self, position: tuple[int, int], radius: int = 9, color: Color = Color.BLACK.value, thickness:int = -1):
        super().__init__(position, color, thickness)
        self.radius = radius

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Circle\nPosition: {self.position}\nRadius: {self.radius}\nColor: {self.color}"

    # def getCenter(self) -> int:
    #     return self.getPosition()
    # def setCenter(self, center: tuple[int, int]):
    #     self.center = center
    #     setPosition(center)
    #override
    def setPosition(self, position: tuple[int, int]):
        # self.center = position
        super().setPosition(position)

    def getRadius(self) -> int:
        return self.radius
    def setRadius(self, radius: int):
        self.radius = radius

    def draw(self, window):
        # negative value for thickness means fill
        cv2.circle(window, self.position, self.radius, self.color, self.thickness)

    def cast(self, circle_based_shape: type):
        # if type not in [Circle, Triangle, Square, Pentagon, Hexagon]:
        #     raise Exception("Not circle-based shape")
        return circle_based_shape(position=self.position, radius=self.radius, color=self.color, thickness=self.thickness)

    # def copy(self):
    #     return self.getShape()(self.position, self.radius, self.color, self.thickness)

class Cross(Circle):
    def __init__(self, position: tuple[int, int], radius: int = 4, color: Color = Color.BLACK.value, thickness: int = 1):
        super().__init__(position, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Cross\nPosition: {self.position}\nRadius: {self.radius}\nColor: {self.color}"

    def draw(self, window):
        cv2.line(window,
                 [int(self.position[0] - self.radius * np.cos(0.25 * np.pi)), int(self.position[1] - self.radius * np.sin(0.25 * np.pi))],
                 [int(self.position[0] - self.radius * np.cos(1.25 * np.pi)), int(self.position[1] - self.radius * np.sin(1.25 * np.pi))],
                 self.color, self.thickness)
        cv2.line(window,
                 [int(self.position[0] - self.radius * np.cos(0.75 * np.pi)), int(self.position[1] - self.radius * np.sin(0.75 * np.pi))],
                 [int(self.position[0] - self.radius * np.cos(-0.25 * np.pi)), int(self.position[1] - self.radius * np.sin(-0.25 * np.pi))],
                 self.color, self.thickness)


class Triangle(Circle):
    def __init__(self, position: tuple[int, int], radius: int = 9, color: Color = Color.BLACK.value, thickness: int = -1):
        super().__init__(position, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Triangle\n"

    def draw(self, window):
        sides = 3
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.position[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.position[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(window, pts, color=self.color)
        else:
            cv2.polylines(window, pts, isClosed=True, color=self.color, thickness=self.thickness)


class Square(Circle):
    def __init__(self, position: tuple[int, int], radius: int = 9, color: Color = Color.BLACK.value, thickness: int = -1):
        super().__init__(position, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Square\n"

    def draw(self, window):
        sides = 4
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.position[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.position[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(window, pts, color=self.color)
        else:
            cv2.polylines(window, pts, isClosed=True, color=self.color, thickness=self.thickness)
       
class Pentagon(Circle):
    def __init__(self, position: tuple[int, int], radius: int = 9, color: Color = Color.BLACK.value, thickness: int = -1):
        super().__init__(position, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Pentagon\n"
    

    def draw(self, window):
        sides = 5
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.position[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.position[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(window, pts, color=self.color)
        else:
            cv2.polylines(window, pts, isClosed=True, color=self.color, thickness=self.thickness)

class Hexagon(Circle):
    def __init__(self, position: tuple[int, int], radius: int = 9, color: Color = Color.BLACK.value, thickness: int = -1):
        super().__init__(position, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Hexagon\n"
    
    def draw(self, window):
        sides = 6
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.position[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.position[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(window, pts, color=self.color)
        else:
            cv2.polylines(window, pts, isClosed=True, color=self.color, thickness=self.thickness)


class Rectangle(Shape):
    def __init__(self, point_1: tuple[int, int], point_2: tuple[int, int], color: Color = Color.BLACK.value, thickness:int = 3):
        super().__init__(None, color, thickness)
        self.point_1 = point_1
        self.point_2 = point_2

    def getPt1(self) -> int:
        return self.point_1

    def setPt1(self, point_1:tuple[int, int]):
        self.point_1 = point_1

    def getPt2(self) -> int:
        return self.point_2

    def setPt2(self, point_2:tuple[int, int]):
        self.point_2 = point_2

    def getCenter(self) -> tuple[int, int]:
        return [0.5 * (self.point_1[0] + self.point_2[0]), 0.5 * (self.point_1[1] + self.point_2[1])]

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Rectangle\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color}"

    def draw(self, window):
        # negative value for thickness means fill
        cv2.rectangle(window, self.point_1, self.point_2, self.color, self.thickness)
        # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        # pts = pts.reshape((-1,1,2))
        # cv.polylines(img,[pts],True,(0,255,255))

class Line(Rectangle):
    def __init__(self, point_1:tuple[int, int], point_2:tuple[int, int], color = Color.BLACK.value, thickness = 3):
        super().__init__(point_1, point_2, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Line\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color}"

    def draw(self, window):
        cv2.line(window, self.point_1, self.point_2, self.color, self.thickness)


def randomShape(w, h) -> Circle:
    color = [Color.RED.value, Color.GREEN.value, Color.BLUE.value, Color.YELLOW.value, Color.CYAN.value, Color.MAGENTA.value][
        random.randint(0, 5)]
    shape = [Circle, Triangle, Square, Pentagon, Hexagon][random.randint(0, 4)]
    position = np.random.randint([0, 0], [w, h])
    return shape(position=position, color=color, thickness=-1)


if __name__ == "__main__":
    
    sides = 5
    angle = 2*np.pi / sides
    radius = 5
    center = (0, 0)

    p1 = (center[0] - radius * np.sin(0.5*angle), center[1] - radius * np.cos(0.5*angle))
    p2 = (center[0] + radius * np.sin(0.5*angle), center[1] - radius * np.cos(0.5*angle))
    p3 = ()
    p4 = (center[0], center[1] + radius)
    p5 = ()

    print(f"p1 = {p1}")
    print(p2)
    print(p3)
    print(p4)
    print(p5)
    

    for i in range(sides):
        print(center[0] + radius * np.cos(-0.5 * np.pi + (i-0.5) * angle), center[1] + radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))

    exit()


    canvas = np.ones((720, 640, 3), dtype="uint8")
    # pts = [((10,5),(20,30),(70,20),(50,10))] # does not work
    pts = np.array([((10,5),(20,30),(70,20),(50,10))])

    cv2.polylines(canvas, pts, True, (255, 0, 0), 5)

    while True:
        cv2.imshow("image", canvas)

        cv2.waitKey(300)
        if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:        
            break


    cv2.destroyAllWindows() # Garde-fou