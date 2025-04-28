###
# window.py
# Useful view classes

# Opencv values doc: https://docs.opencv.org/4.5.0/d4/dd5/highgui_8hpp.html

from shape import *
from typing import List
from utils import Color

from abc import ABC, abstractmethod
import numpy as np
import cv2
import os
import ast


def randomShape() -> Circle:
    color = [Color.RED.value, Color.GREEN.value, Color.BLUE.value, Color.YELLOW.value, Color.CYAN.value, Color.MAGENTA.value][
        random.randint(0, 5)]
    shape = [Circle, Triangle, Square, Pentagon, Hexagon][random.randint(0, 4)]
    position = np.random.randint([0, 0], [w, h])
    return shape(position=position, color=color)

class Window(ABC):
    def __init__(self, width:int, height:int, name:str):
        self.height = height
        self.width = width
        self.name = name
        self.window = None
        self._resetWindow()
        cv2.imshow(self.name, self.window)

    @abstractmethod
    def update(self):
        pass

    def show(self, front=False):
        cv2.imshow(self.name, self.window)
        if front: self.__toFront()

    def destroyWindow(self):
        self.update()
        cv2.destroyWindow(self.name)

    def __toFront(self):
        cv2.setWindowProperty(self.name, cv2.WND_PROP_TOPMOST, 1)

    def _resetWindow(self):
        self.window = np.ones((self.height, self.width, 3), dtype="uint8")*Color.BACKGROUND.value

    def setDimensions(self, width: int, height: int):
        self.width = width
        self.height = height
        self.view.setDimensions(width, height)

    def getDimensions(self) -> tuple[int, int]:
        return self.width, self.height

    def getName(self) -> str:
        return self.name

    def getWidth(self) -> int:
        return self.width
    def getHeight(self) -> int:
        return self.height


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


class Selector(Window):
    def __init__(self, width:int=200, height:int=200, name:str = None):
        super().__init__(width, height, name if name is str else f"{id(self)}")
        self.shape = Circle(position=(100,100), radius=100, color = (0, 0, 255), thickness = -1)
        self.color = (0, 0, 255)

        cv2.createTrackbar('color', self.name, 0, 5, self.__colorTrackbarCallback)
        cv2.createTrackbar('shape', self.name, 0, 4, self.__shapeTrackbarCallback)

    def update(self):
        self._resetWindow()
        self.shape.draw(self.window)
        self.show()

    def __colorTrackbarCallback(self, value:int):
        self.setColor(color_selection[value], trackbar_update=False)

    def __shapeTrackbarCallback(self, value:int):
        self.setShapeType(shape_selection[value], trackbar_update=False)

    def __setColorTrackbar(self, color:tuple[int,int,int]):
        cv2.setTrackbarPos('color', self.name, color_selection[color])

    def __setShapeTrackbar(self, shape:type):
        cv2.setTrackbarPos('shape', self.name, shape_selection[type(shape)])

    def getShapeType(self) -> type:
        return type(self.shape)

    def getShape(self) -> Circle:
        return self.shape

    def setShape(self, shape: Circle, trackbar_update=True):
        self.shape = self.shape.cast(type(shape))
        self.shape.setColor(shape.getColor())
        if trackbar_update:
            self.__setShapeTrackbar(self.getShape())
            self.__setColorTrackbar(self.getColor())
        self.update()

    def setShapeType(self, shape: type, trackbar_update=True):
        self.shape = self.shape.cast(shape)
        if trackbar_update: self.__setShapeTrackbar(self.getShape())
        self.update()

    def getColor(self) -> tuple[int, int, int]:
        return self.shape.getColor()

    def setColor(self, color: tuple[int, int, int], trackbar_update=True):
        self.shape.setColor(color)
        if trackbar_update: self.__setColorTrackbar(self.getColor())
        self.update()


class Screen(Window):
    def __init__(self, width: int = 720, height: int = 720, name: str = None, selector=False):
        super().__init__(width, height, name if name is str else f"{id(self)}")
        self.shapes: List[Shape] = []

        if selector:
            self.selector = Selector()
            cv2.setMouseCallback(self.name, self.__mouseCallback)

    def __str__(self, view: bool = True, model:bool = True) -> str:
        if view: print(f"- View -\nWidth: {self.width}, Height: {self.height}\n")
        if model: print("\n".join(str(s) for s in self.shapes))

    def update(self, front=True):
        self._resetWindow()
        for s in self.shapes:
            s.draw(self.window)
        self.show(front=front)

    #override
    def show(self, front=False):
        if self.selector: self.selector.show(front=front)
        super().show(front=front)

    # override
    def destroyWindow(self):
        if self.selector: self.selector.destroyWindow()
        super().destroyWindow()

    def addShape(self, shape: Drawable):
        self.shapes.append(shape)

    def addShapes(self, shapes: List[Drawable]):
        self.shapes.extend(shapes)

    def setShapes(self, shapes: List[Drawable]):
        self.shapes = shapes

    def getShapes(self) -> List[Drawable]:
        return self.shapes

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
                file.write(f"{s.toDict()}\n")
    
    def __load_model(self, filename):
        self.shapes: List[Shape] = []
        with open(filename, 'r') as file:
            for line in file:
                sample_dict = ast.literal_eval(line)
                self.addShape(sample_dict['shape'](sample_dict['position'],
                                       sample_dict['color'], sample_dict['thickness']))
        self.update()

    def removeShape(self, shape: Circle):
        self.shapes.remove(shape)
        self.update()

    def __closestShape(self, x, y):
        if len(self.shapes) == 0:
            return None
        closest_shape = self.shapes[0]
        closest_distance_criteria = np.abs(closest_shape.x - x) + np.abs(closest_shape.y - y)
        for s in self.shapes[1:]:
            v = np.abs(s.x - x) + np.abs(s.y - y)
            if v < closest_distance_criteria:
                closest_shape = s
                closest_distance_criteria = v
        return closest_shape

    def __detectColor(self, x, y):
        return np.any(self.window[y, x, :] != [Color.BACKGROUND.value, Color.BACKGROUND.value, Color.BACKGROUND.value])

    def __mouseCallback(self, event, x, y, flags, param):
        # print(x, y, event, flags, param)
        if event == 1:
            # print(f"Left-button pressed on {(x,y)}")
            if self.__detectColor(x, y):
                self.removeShape(self.__closestShape(x, y))
                print("Shape removed")
            else:
                self.addShape(self.selector.getShape().clone(diff_params={"position":(x,y), "radius":9}))
                print("Shape added")
            
        elif event == 2:
            # print(f"Right-button pressed on {(x,y)}")
            if self.__detectColor(x, y):
                selected_shape = self.__closestShape(x, y)
                # print(selected_shape)
                self.selector.setShape(selected_shape)
                print(f"Shape selected:\n{selected_shape}")
            else:
                print("No shape selected")
        elif event == 3:
            # pt = np.random.randint([0, 0], [w, h]) ## Avoid collision with other shape ?
            created_shape = randomShape()
            self.addShape(created_shape)
            self.selector.setShape(created_shape)
            print("Random shape created")
        self.update()


    def waitEvent(self, time=30, verbose=False):
        # 1: Nothing
        # 0: Window closed
        # < 0: All events that should terminate the running

        keys = cv2.waitKey(time)
        if cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1:
            return 0

        if verbose and keys != -1: print(f"keys = {keys}")

        if keys == 27:  # Escape key
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
        elif keys == 32:  # spacebar
            return 2
        return 1

if __name__ == "__main__":
    from utils import Color
    import numpy as np

    # w, h = extractMonitorDimensions()
    # w, h = 640, 480
    screen = Screen(selector=True)
    w, h = screen.getDimensions()
    screen.show()

    while True:
        criteria = screen.waitEvent(time=100, verbose=False)
        if criteria == 0:
            break

        screen.addShape(randomShape())

        screen.update()
    screen.destroyWindow() # Garde-fou
