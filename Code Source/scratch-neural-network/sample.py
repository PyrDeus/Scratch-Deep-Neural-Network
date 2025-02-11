

from shape import Drawable, Circle, Triangle, Square, Pentagon, Hexagon  

shape_classes = {
    'square': Square,
    'circle': Circle,
    'triangle': Triangle,
    'pentagon': Pentagon,
    'hexagon': Hexagon
}

# Not in RGB, OpenCV uses BGR
color_classes = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'cyan': (255, 255, 0),
    'magenta': (255, 0, 255),
    'orange': (0, 165, 255),
    'purple': (128, 0, 128),
    'pink': (203, 192, 255),
    'brown': (42, 42, 165),
    'gray': (128, 128, 128)
}


class Sample2D(Drawable):
    def __init__(self, position:tuple[int, int], shape:str="square", color:str="red", radius:int=9):
        self.position = position
        
        self.color = color_classes[color]
        self.__color_label = color

        self.shape = shape_classes[shape](center=position, radius=radius, color=self.color, thickness=-1)
        self.__shape_label = shape

    def __str__(self):
        return f"Class Sample\nShape Label: {self.__shape_label}\nColor Label: {self.__color_label}"
    
    def getColor(self) -> tuple[int, int, int]:
        return self.color
    
    def getColorLabel(self) -> str:
        return self.__color_label
    
    def getShape(self):
        return type(self.shape)
    
    def getShapeLabel(self):
        return self.__shape_label
    
    def getShapeLabel(self):
        return self.shape

    def draw(self, canvas):
        self.shape.draw(canvas)
    
    def hasLabel(self, label):
        return label == self.__color_label or label == self.__shape_label

