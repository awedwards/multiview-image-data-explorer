class SegmentationObject():

    def __init__(self, cx, cy, boundingbox):

        self.cx = cx
        self.cy = cy
        self.bb = boundingbox
        self.index = None

class SegmentationIndex():

    def __init__(self):

        self.index = {}
    
    def add_object(self, ob):

        self.index[(ob.cx, ob.cy)] = ob.index

    def remove_object(self, ob):

        del self.index[(ob.cx, ob.cy)]