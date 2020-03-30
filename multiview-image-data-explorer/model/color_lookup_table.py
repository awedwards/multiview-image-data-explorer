import numpy as np

class ColorLUT():

    def __init__(self, cid, label, index, color):

        self.cid = cid
        self.label = label
        self.index = index
        self.color = color
    
    @property
    def index(self):
        return self.__index
    
    @index.setter
    def index(self, value):
        
        if value is not None:
            value = np.vstack(value)
            if 0 in value.shape:
                self.__index = None
            elif value.shape[1] == 2:
                self.__index = value
            elif value.shape[0] == 2:
                self.__index = np.transpose(value)
            else:
                raise(IndexError)
        else:
            self.__index = value