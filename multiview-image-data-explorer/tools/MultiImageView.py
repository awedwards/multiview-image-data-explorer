import pyqtgraph as pg

class MultiColorImageView(pg.ImageView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lut = None
        self.tVals = None

    def updateImage(self, autoHistogramRange=True):
        super().updateImage(autoHistogramRange)
        self.getImageItem().setLookupTable(self.lut)