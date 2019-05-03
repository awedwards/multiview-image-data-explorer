import pandas as pd
import operator
from functools import reduce
import numpy as np
import h5py
df = pd.read_csv("D:\\Austin\CD8a_CD4_44784_Image_Export_01\\full_object_feature_output.csv", index_col=False,sep=',')
from sklearn.cluster import DBSCAN
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

results = [ df[df["Predicted Class"] == "CD4"], df[df["Predicted Class"] == "CD8"]]

results = reduce(lambda  left,right: pd.merge(left,right,
                                                how='outer'), results)

cx = results["Center of the object_1"]
cy = results["Center of the object_0"]

X = np.vstack((cx, cy))

min_dist = 20
min_neighbors = 2
db = DBSCAN(eps=min_dist, min_samples=min_neighbors).fit(np.transpose(X))
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

#print('Estimated number of clusters: %d' % n_clusters_)
