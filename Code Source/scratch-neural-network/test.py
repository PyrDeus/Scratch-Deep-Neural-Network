#!/usr/local/bin/python3
import numpy as np
import cv2

class Screen:
    def __init__(self, width = 640, height = 480, framerate=5):
        self.width = width
        self.height = height
        self.framerate = framerate

    def display_attributes(self):
        print(f"Width: {self.width}, Height: {self.height}\nFramerate:  {self.framerate}")
    
    def display(self, model):
        while True:
            npimage = model() # Update the model
            
            cv2.imshow('image', npimage) # Show
            cv2.waitKey(self.framerate)
            
            # Exit the loop if the window is closed
            if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
                break
        cv2.destroyAllWindows() # Remove all windows (garde-fou)

    def run(self):

        while True:
            # Get a numpy array to display from the simulation
            npimage=getFrame()

            cv2.imshow('image',npimage)
            cv2.waitKey(10)
            if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
                break
        cv2.destroyAllWindows()


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