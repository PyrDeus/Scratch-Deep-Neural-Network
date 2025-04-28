

from shape import Cross, Shape
from utils import randomShape

class Sampler:
    def __init__(self, *level):
        self.shapes:List[Shape] = level['shapes']
        self.width:int = level['width']
        self.height:int = level['height']
        self.samples:List[Cross] = None

    def __closestShapeColor(self, position:tuple[int, int]):
        x, y = position
        if len(self.shapes) == 0:
            return None
        closest_shape = self.shapes[0].getColor()
        closest_distance_criteria = np.abs(closest_shape.x - x) + np.abs(closest_shape.y - y)
        for s in self.shapes[1:]:
            v = np.abs(s.x - x) + np.abs(s.y - y)
            if v < closest_distance_criteria:
                closest_shape = s.getColor()
                closest_distance_criteria = v
        return closest_shape.getShape(), closest_shape.getColor()

    def __createRandomCross(self):
        position = np.random.randint([0, 0], [self.width, self.height])
        shape, color = self.__closestShapeColor(position)
        new_sample = shape(position=position, color=self.__closestShapeColor(position))
        self.samples.append(new_sample)

    def create_datas(self, number_samples, train_test_ratio = 0.8, train_validation_ratio=0.2):
        for _ in range(number_samples):
            self.__createRandomCross()

        # Ration of datasets: train = 0.8 * 0.8 = 0.64, val = 0.8 * 0.2 = 0.16, test = 0.2
        train_slice = number_samples * train_test_ratio * (1-train_validation_ratio)
        validation_slice = number_samples * train_test_ratio * train_validation_ratio
        test_slice = number_samples * (1-train_test_ratio)

        train_set = self.samples[:train_slice]
        del self.samples[:train_slice]
        validation_set = self.samples[:validation_slice]
        del self.samples[:validation_slice]
        test_set = self.samples[:test_slice]
        del self.samples[:test_slice]

        return train_set, validation_set, test_set
