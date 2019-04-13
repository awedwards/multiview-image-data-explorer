import numpy as np

class CellObject():

    def __init__(self, cx, cy):

        self.cx = cx
        self.cy = cy
        self.index = (cx, cy)

    @property
    def index(self):
        return self.__index
    
    @index.setter
    def index(self, value):
        self.__index = value
        #self.__index['x'] = np.array(value[0])
        #self.__index['y'] = np.array(value[1])

child = CellObject(1.0, 2.0)
print(child.index)