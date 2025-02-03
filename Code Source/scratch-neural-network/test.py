#!/usr/local/bin/python3
import numpy as np
import cv2
from typing import List
from abc import ABC, abstractmethod

class Screen:
    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height
        self.view = ScreenView(width, height)
        self.model = ScreenModel()

    def __str__(self, view: bool = True, model:bool = True) -> str:
        return f"- View -\n{self.view}" * int(view) + f"- Model -\n{self.model}" * int(model) 
    
    def setDimensions(width: int, height: int):
        self.width = width
        self.height = height
        self.view.setDimensions(width, height)
    
    def getDimensions() -> tuple[int, int]:
        return self.width, self.height

    def addShape(self, shape: Shape):
        self.model.addShape(shape)

    def addShapes(self, shapes: List[Shape]):
        self.model.addShapes(shapes)

    def getShapes(self) -> List[Shape]:
        return self.model.getShapes()
    
    def setShapes(self, shapes: List[Shape]):
        self.model.setShapes(shapes)

    def run(self, framerate=10):
        while True:
            # Get a numpy array to display from the simulation
            npimage=getFrame()

            cv2.imshow('image',npimage)
            cv2.waitKey(framerate)
            if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
                break
        cv2.destroyAllWindows() # Garde-fou

    def old_run(self, framerate=10):
        while True:
            # Get a numpy array to display from the simulation
            npimage=getFrame()

            cv2.imshow('image',npimage)
            cv2.waitKey(framerate)
            if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
                break
        cv2.destroyAllWindows() # Garde-fou

    def update(self):
        # Draw all from scratch


class ScreenView:
    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Width: {self.width}, Height: {self.height}"

class ScreenModel:
    def __init__(self):
        self.shapes: List[Shape] = []

    def __str__(self) -> str:
        return "\n".join(str(s) for s in self.shapes)

    def addShape(self, shape: Shape):
        self.shapes.append(shape)

    def addShapes(self, shapes: List[Shape]):
        self.shapes.extend(shapes)

    def getShapes(self) -> List[Shape]:
        return self.shapes

    def setShapes(self, shapes: List[Shape]):
        #self.shapes = [] # Needed?
        self.shapes = shapes 


class Shape:
    def __init__(self, position):
        self.position = position
    
    def __str__(self) -> str:
        return f"Class Shape\nSubclass None\nPosition: {self.position}"


def sin2d(x,y):
    """2-d sine function to plot"""
    return np.sin(x) + np.cos(y)

def getFrame():
    """Generate next getFrame.z of simulation as numpy array"""

    # Create data on first call only
    if getFrame.z is None:
        xx, yy = np.meshgrid(np.linspace(0,2*np.pi,w), np.linspace(0,2*np.pi,h))
        getFrame.z = sin2d(xx, yy)
        getFrame.z = cv2.normalize(getFrame.z,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # Just roll data for subsequent calls
    getFrame.z = np.roll(getFrame.z,(1,2),(0,1))
    return getFrame.z


w, h = 640, 480
getFrame.z = None

screen = Screen()
screen.run()