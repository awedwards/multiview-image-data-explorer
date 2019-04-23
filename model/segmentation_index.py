"""
@author: Austin Edwards

Class objects for storing segmentation object information, including indexes

"""

class SegmentationObject():

    """ Class containing information about segmentation objects. Stores
        object center, object id number, bounding box vertices, and
        index of the object
    """

    def __init__(self, i, cx, cy, boundingbox):
        
        self.id = i
        self.cx = cx
        self.cy = cy
        self.bb = boundingbox
        self.index = None

class SegmentationIndex():

    """ Class for fast look up of object indexes """

    def __init__(self):

        self.index = {}
    
    def add_object(self, ob):
        """ Adds object index to dictionary """
        self.index[ob.id] = ob.index

    def remove_object(self, ob):
        """ Removes object index from dictionary by id """
        del self.index[ob.id]