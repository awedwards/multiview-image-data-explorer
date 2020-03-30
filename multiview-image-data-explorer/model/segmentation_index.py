"""
@author: Austin Edwards

Class objects for storing segmentation object information, including indexes

"""

class SegmentationObject():

    """ Class containing information about segmentation objects. Stores
        object center, object id number, bounding box vertices, and
        index of the object
    """

    def __init__(self, i, cx, cy, boundingbox, k):
        
        self.id = i
        self.cx = cx
        self.cy = cy
        self.bb = boundingbox
        self.index = None
        self._class = k

class SegmentationIndex():

    """ Class for fast look up of object indexes """

    def __init__(self):

        self.index = {}
        self._class = {}
        self.objs = {}
    
    def add_object(self, ob):
        """ Adds object index to dictionary """
        self.index[ob.id] = ob.index
        self._class[ob.id] = ob._class
        self.objs[ob.id] = ob

    def remove_object(self, ob):
        """ Removes object index from dictionary by id """
        del self.index[ob.id]
        del self._class[ob.id]
        del self.objs[ob.id]