import pandas as pd
import operator
from functools import reduce
import numpy as np
import h5py
#df = pd.read_csv("D:\\Austin\CD8a_CD4_44784_Image_Export_01\\full_object_feature_output.csv", index_col=False,sep=',')
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
#f = h5py.File("D:\\Austin\CD8a_CD4_44784_Image_Export_01\\full.hdf5")

#print(f.keys)

#result = df[(df['Predicted Class']=='CD4') | (df['Predicted Class']=='CD8')]
#print(result['object_id'].values)

#import initExample ## Add path to library (just for examples; you do not need this)

#import pyqtgraph as pg
#import pyqtgraph.examples
#pyqtgraph.examples.run()
#p = pg.Point([0,1])
#print(p*3)

#idx = [False]*len(df)
#idx[0] = True
#idx[3] = True
#print(-idx)
"""
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

for c in colors:
    c = c.lstrip("#")

    print ( tuple( int(c[i:i+2], 16) for i in [0, 2, 4]) )

print(colors)               
"""

#f = h5py.File("D:\\Austin\\test_data\\tmp_3920_8047_3858_7920_Object Predictions.h5")

#print(np.squeeze(f["exported_data"]).shape)
import pyqtgraph.examples
pyqtgraph.examples.run()