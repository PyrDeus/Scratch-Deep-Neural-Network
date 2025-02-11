###
# shape.py
# Contains shapes and useful classes to use on the canvas of the Screen class (screen.py) 


from utils import *

import cv2
from abc import ABC, abstractmethod
import numpy as np

class Shape(ABC):
    def __init__(self, color:Color = Color.BLACK, thickness:int = 3):
        self.color = color
        self.thickness = thickness
    
    def __str__(self) -> str:
        return f"Class Shape\nSubclass None\nPosition: {self.position}"
    
    @abstractmethod
    def draw(self, canvas):
        pass

    def setColor(self, color:Color):
        self.color = color
    def getColor(self) -> Color:
        return self.color

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

    def draw(self, canvas):
        # negative value for thickness means fill
        cv2.rectangle(canvas, self.point_1, self.point_2, self.color, self.thickness)
        # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        # pts = pts.reshape((-1,1,2))
        # cv.polylines(img,[pts],True,(0,255,255))

class Line(Rectangle):
    def __init__(self, point_1:tuple[int, int], point_2:tuple[int, int], color = Color.BLACK, thickness = 3):
        super().__init__(point_1, point_2, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Line\nPoint 1: {self.point_1}\nPoint 2: {self.point_2}\nColor: {self.color}"

    def draw(self, canvas):
        cv2.line(canvas, self.point_1, self.point_2, self.color, self.thickness)


class Triangle(Circle):
    def __init__(self, center, radius, color = Color.BLACK, thickness = 3):
        super().__init__(center, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Triangle\n"

    def draw(self, canvas):
        sides = 3
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.center[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.center[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(canvas, pts, color=self.color)
        else:
            cv2.polylines(canvas, pts, isClosed=True, color=self.color, thickness=self.thickness)
        
class Square(Circle):
    def __init__(self, center, radius, color = Color.BLACK, thickness = 3):
        super().__init__(center, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Square\n"

    def draw(self, canvas):
        sides = 4
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.center[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.center[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(canvas, pts, color=self.color)
        else:
            cv2.polylines(canvas, pts, isClosed=True, color=self.color, thickness=self.thickness)
       
class Pentagon(Circle):
    def __init__(self, center, radius, color = Color.BLACK, thickness = 3):
        super().__init__(center, radius, color, thickness)


    def __str__(self) -> str:
        return f"Class Shape\nSubclass Pentagon\n"
    

    def draw(self, canvas):
        sides = 5
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.center[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.center[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(canvas, pts, color=self.color)
        else:
            cv2.polylines(canvas, pts, isClosed=True, color=self.color, thickness=self.thickness)
        


class Hexagon(Circle):
    def __init__(self, center, radius, color = Color.BLACK, thickness = 3):
        super().__init__(center, radius, color, thickness)

    def __str__(self) -> str:
        return f"Class Shape\nSubclass Hexagon\n"
    
    def draw(self, canvas):
        sides = 6
        angle = 2*np.pi / sides
        
        pts = np.array([[ ( int(self.center[0] - self.radius * np.cos(-0.5 * np.pi + (i-0.5) * angle)), int(self.center[1] - self.radius * np.sin(-0.5 * np.pi + (i-0.5) * angle))) for i in range(sides)] ])

        if self.thickness < 0:
            cv2.fillPoly(canvas, pts, color=self.color)
        else:
            cv2.polylines(canvas, pts, isClosed=True, color=self.color, thickness=self.thickness)



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