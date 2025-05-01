import pandas as pd

from shape import Shape, Circle, Triangle, Square, Pentagon, Hexagon, randomShape
from window import Canvas, Selector
from utils import Color, saveCSVLayout, loadCSVLayout, askNewLevelFile, askLevelFile

from typing import List
import cv2
import numpy as np


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

class Level:
    def __init__(self, edition_mode=True, render=True):
        self.edition_mode = edition_mode

        self.shapes: List[Shape] = []
        self.canvas = Canvas(name="Canvas", shapes=self.shapes, render=render)

        if edition_mode:
            cv2.setMouseCallback(self.canvas.getName(), self.__mouseCallback)

            self.edition_shape = Circle(position=(100, 100), radius=100, color=(0, 0, 255), thickness=-1)
            self.selector = Selector(name = "Selector", edition_shape = self.edition_shape)
            cv2.createTrackbar('color', self.selector.getName(), 0, 5, self.__colorTrackbarCallback)
            cv2.createTrackbar('shape', self.selector.getName(), 0, 4, self.__shapeTrackbarCallback)
        else:
            self.samples: List[Shape] = []
            self.canvas.setSamples(self.samples)


    def createDatas(self, number_samples, train_test_ratio=0.8, train_validation_ratio=0.2):
        for _ in range(number_samples):
            self.__createRandomSample()

        # Ration of datasets: train = 0.8 * 0.8 = 0.64, val = 0.8 * 0.2 = 0.16, test = 0.2
        train_nb = int(number_samples * train_test_ratio * (1 - train_validation_ratio))
        validation_nb = int(number_samples * train_test_ratio * train_validation_ratio)
        test_nb = int(number_samples * (1 - train_test_ratio))

        samples_df = self.samplesToDataframe()

        train_set = samples_df[:train_nb]
        validation_set = samples_df[train_nb:train_nb + validation_nb]
        test_set = samples_df[train_nb + validation_nb:train_nb + validation_nb + test_nb]
        return train_set, validation_set, test_set

    def __createRandomSample(self):
        x, y = np.random.randint([0,0], self.canvas.getDimensions())
        closest_shape = self.closestShape(x, y)
        new_sample = closest_shape.getShapeType()(position=(x, y),
                                                    color=closest_shape.getColor(),
                                                    thickness=1)
        self.samples.append(new_sample)

    def addRandomShape(self):
        s = randomShape(self.canvas.getWidth(), self.canvas.getHeight())
        self.addShape(s)
        self.setEditionShape(s.clone(diff_params={"position": (100,100), "radius":100}))
        self.canvas.update()
        self.selector.update()

    def shapesToDataframe(self):
        data = {"shape": [], "color": [], "x": [], "y": [], "thickness": []}
        for s in self.shapes:
            data["shape"].append(shape_selection[s.getShapeType()])
            data["color"].append(color_selection[s.getColor()])
            data["x"].append(s.x)
            data["y"].append(s.y)
            data["thickness"].append(s.getThickness())
        return pd.DataFrame(data)

    def samplesToDataframe(self):
        data = {"shape": [], "color": [], "x": [], "y": [], "thickness": []}
        for s in self.samples:
            data["shape"].append(shape_selection[s.getShapeType()])
            data["color"].append(color_selection[s.getColor()])
            data["x"].append(s.x)
            data["y"].append(s.y)
            data["thickness"].append(s.getThickness())
        return pd.DataFrame(data)

    def dataframeToShapes(self, dataframe: pd.DataFrame):
        self.shapes = []
        data = pd.DataFrame.to_dict(dataframe)
        shape_nb = len(data['shape'])
        for index in range(shape_nb):
            self.shapes.append(
                shape_selection[data['shape'][index]](
                    position=(data['x'][index], data['y'][index]),
                    color=color_selection[data['color'][index]],
                    thickness=data['thickness'][index],
                )
            )
        self.canvas.setShapes(self.shapes)

    def saveLayout(self, file_path):
        saveCSVLayout(file_path, self.shapesToDataframe())

    def loadLayout(self, file_path):
        self.dataframeToShapes(loadCSVLayout(file_path))

    def addShape(self, shape: Shape):
        self.shapes.append(shape)
        self.canvas.update()

    def addShapes(self, shapes: List[Shape]):
        self.shapes.extend(shapes)
        self.canvas.update()

    def setShapes(self, shapes: List[Shape]):
        self.shapes = shapes
        self.canvas.update()

    def getShapes(self) -> List[Shape]:
        return self.shapes

    def removeShape(self, shape: Circle):
        self.shapes.remove(shape)
        self.canvas.update()

    def closestShape(self, x, y):
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
        return np.any(self.canvas[y, x] != [Color.BACKGROUND.value, Color.BACKGROUND.value, Color.BACKGROUND.value])


    def __mouseCallback(self, event, x, y, flags, param):
        # print(x, y, event, flags, param)
        if event == 1:
            # print(f"Left-button pressed on {(x,y)}")
            if self.__detectColor(x, y):
                self.removeShape(self.closestShape(x, y))
                # print("Shape removed")
            else:
                self.addShape(self.edition_shape.clone(diff_params={"position": (x, y), "radius": 9}))
                # print("Shape added")
        elif event == 2:
            # print(f"Right-button pressed on {(x,y)}")
            if self.__detectColor(x, y):
                selected_shape = self.closestShape(x, y)
                # print(selected_shape)
                self.setEditionShape(selected_shape.copy())
                # print(f"Shape selected:\n{selected_shape}")
            # else:
                # print("No shape selected")
        elif event == 3:
            # pt = np.random.randint([0, 0], [w, h]) ## Avoid collision with other shape ?
            self.addRandomShape()
            # print("Random shape created")
        self.canvas.update()

    def __colorTrackbarCallback(self, value: int):
        self.setEditionColor(color_selection[value], trackbar_update=False)
        self.selector.update()

    def __shapeTrackbarCallback(self, value: int):
        self.setEditionShapeType(shape_selection[value], trackbar_update=False)
        self.selector.update()

    def getEditionShapeType(self) -> type:
        return type(self.edition_shape)

    def getEditionShape(self) -> Circle:
        return self.edition_shape

    def setEditionColor(self, color: tuple[int, int, int], trackbar_update=True):
        self.edition_shape.setColor(color)
        # self.selector.setEditionShape(self.edition_shape)

        if trackbar_update: self.selector.setEditionColorTrackbar(color_selection[self.getEditionColor()])
        self.selector.update()

    def setEditionShape(self, shape: Circle, trackbar_update=True):
        self.edition_shape = self.edition_shape.cast(type(shape))
        self.edition_shape.setColor(shape.getColor())
        self.selector.setEditionShape(self.edition_shape)

        if trackbar_update:
            self.selector.setEditionShapeTypeTrackbar(shape_selection[self.getEditionShapeType()])
            self.selector.setEditionColorTrackbar(color_selection[self.getEditionColor()])
        self.selector.update()

    def setEditionShapeType(self, shape: type, trackbar_update=True):
        self.edition_shape = self.edition_shape.cast(shape)
        self.selector.setEditionShape(self.edition_shape)

        if trackbar_update: self.selector.setEditionShapeTypeTrackbar(self.getEditionShapeType())
        self.selector.update()

    def getEditionColor(self) -> tuple[int, int, int]:
        return self.edition_shape.getColor()

    def waitEvent(self, time=30, verbose=False):
        # 1: Nothing
        # 0: Window closed
        # < 0: All events that should terminate the running

        keys = cv2.waitKey(time)
        if cv2.getWindowProperty(self.canvas.getName(), cv2.WND_PROP_VISIBLE) < 1:
            return 0

        if verbose and keys != -1: print(f"keys = {keys}")

        if keys == 27:  # Escape key
            return 0
        elif keys == ord('s'):
            if self.edition_mode:
                filename = askNewLevelFile()
                self.saveLayout(filename)
                return 1
        elif keys == ord('l'):
            if self.edition_mode:
                file = askLevelFile()
                self.loadLayout(file)
                self.canvas.update()
                return 1
        elif keys == 32:  # spacebar
            return 2
        return 1

    def end(self):
        self.canvas.destroyWindow()
        self.selector.destroyWindow()


if __name__ == "__main__":
    level = Level()

    while True:
        criteria = level.waitEvent(time=100, verbose=False)
        if criteria == 0:
            break

    level.end()