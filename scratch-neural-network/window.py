###
# window.py
# Useful view classes

# Opencv values doc: https://docs.opencv.org/4.5.0/d4/dd5/highgui_8hpp.html

from shape import Shape
from typing import List
from utils import Color

from abc import ABC, abstractmethod
import numpy as np
import cv2
import os
import ast


class Window(ABC):
    def __init__(self, width:int, height:int, name:str=None, render:bool=True):
        self.height = height
        self.width = width
        self.name = name if name is str else f"{id(self)}"
        self.render = render
        if render:
            self._resetWindow()
            cv2.imshow(self.name, self.window)

    def __getitem__(self, *item):
        x, y = item[0]
        return self.window[x, y, :]

    @abstractmethod
    def update(self):
        pass

    def show(self, front=False):
        if self.render:
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


class Selector(Window):
    def __init__(self, edition_shape, width:int=200, height:int=200, name:str = None):
        super().__init__(width, height, name)
        self.edition_shape = edition_shape

    def update(self):
        self._resetWindow()
        self.edition_shape.draw(self.window)
        self.show()

    def setEditionColorTrackbar(self, value:int):
        cv2.setTrackbarPos('color', self.name, value)

    def setEditionShapeTypeTrackbar(self, value:int):
        cv2.setTrackbarPos('shape', self.name, value)

    def setEditionShape(self, shape):
        self.edition_shape = shape


class Canvas(Window):
    def __init__(self, shapes, width: int = 720, height: int = 720, name: str = None, render:bool = True):
        super().__init__(width, height, name, render=render)
        self.samples = None
        self.shapes = shapes


    def __str__(self) -> str:
        print(f"- View -\nWidth: {self.width}, Height: {self.height}\n")

    def update(self, front=True):
        self._resetWindow()
        for s in self.shapes:
            s.draw(self.window)
        self.show(front=front)

    def setShapes(self, shapes):
        self.shapes = shapes
    def getShapes(self):
        return self.shapes

    def setSamples(self, samples):
        self.samples = samples
    def getSamples(self):
        return self.samples

if __name__ == "__main__":
    print("Nothing to show here")
