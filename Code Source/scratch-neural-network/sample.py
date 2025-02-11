

from shape import Shape
from enum import Enum

shape_classes = {
    'square': Square,
    'circle': Circle,
    'triangle': Triangle,
    'pentagon': Pentagon,
    'hexagon': Hexagon
}

# Example usage
favorite_color = Color.GREEN
print(favorite_color)
print(favorite_color.name)
print(favorite_color.value)

    
class Sample():
    def __init__(self, shape:str):
        self.shape = Shape

    def __str__(self):
        return f"Class Sample\nShape Class {type(self.shape)}"
    
    def draw(self, canvas):
        self.shape.draw(canvas)
    

