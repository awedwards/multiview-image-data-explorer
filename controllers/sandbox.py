import pandas as pd
import numpy as np

df = pd.read_csv("D:\\Austin\\CD8a_CD4_45062_Image_Export_04\\full_object_feature_output.csv")

print(df['Predicted Class'].unique())

for i in df['labelimage_oid'].index:
    print(i)