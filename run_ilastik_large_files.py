import sys, io
import os
import h5py
import subprocess
import numpy as np
import tkinter as tk
from tkinter import filedialog, Listbox
from stitch_ilastik_output import stitch
from file_cleanup import cleanup
from pathlib import Path, PurePath
from parse import parse

# dummy GUI for file dialog purposes
root = tk.Tk()
root.withdraw()

file_list = filedialog.askopenfilenames(title="Select input file list")

files = []
with open(file_list[0],"r") as f:
    line = f.readline()
    while line:
        files.append(Path(line.strip()))
        line = f.readline()

param_files = filedialog.askopenfilenames(title='Select parameter file')
params = parse(param_files[0])

for filepath in files:
    
    p = Path(filepath)
    dir_ = p.parent
    file_ = p.name
    
    try:
        overlap = params['overlap']
        decimation_factor = params['decimation_factor']
    except KeyError:
        overlap = 0.02
        decimation_factor = 4 
    
    overlap = float(overlap)
    decimation_factor = int(decimation_factor)
    
    filesep = "/"
    f = h5py.File(filepath,'r')
    
    key = [k for k in f.keys() if k != "__DATA_TYPES__"]
    
    if len(key) > 1:
        print("Only h5 files with a single dataset can be used")
        raise(IndexError)

    d = f[key[0]]
    print(d.shape)
    try:
        t,z,x,y,c=d.shape
    except ValueError:
        x,y,c=d.shape
    new_dim_x = np.floor(x/decimation_factor)
    new_dim_y = np.floor(y/decimation_factor)

    xstart = list(range(0,x,int(new_dim_x * (1-overlap) )))
    if x-xstart[-1] < new_dim_x:
        xstart.pop(-1)

    xend = xstart+new_dim_x
    if xend[-1] < x:
        xend[-1] = x

    ystart = list(range(0,y,int(new_dim_y * (1-overlap) )))
    if y-ystart[-1] < new_dim_y:
        ystart.pop(-1)

    yend = ystart+new_dim_y
    if yend[-1] < y:
        yend[-1] = y
    tmp_file_list = []

    tmp_dir = PurePath(dir_, "tmp")
    
    try:
        os.mkdir(tmp_dir)
    except OSError:
        print ("Creation of directory %s failed" % tmp_dir)
    
    for i in np.arange(len(xstart)):
        for j in np.arange(len(ystart)):
     
            rs = int(xstart[i])
            re = int(xend[i])
            cs = int(ystart[j])
            ce = int(yend[j])       
            
            tmp_filename = "tmp" + "_".join(["",str(rs),str(re),str(cs),str(ce)]) + ".h5"
            with h5py.File(PurePath(tmp_dir, tmp_filename), "w") as out:
                try:
                    dset = out.create_dataset("data", data=d[:,:,rs:re,cs:ce,:])
                except TypeError:
                    dset = out.create_dataset("data", data=d[rs:re,cs:ce,:])
            
            tmp_file_list.append(str(PurePath(tmp_dir, tmp_filename)))
    
    if 'pixel_classifier_filepath' in params:

        pixel_probability_maps = [s[:-3] + "_pixel_probabilities.h5" for s in tmp_file_list]
        cmd_pixel= "/home/bidc/ilastik/run_ilastik.sh --headless"
        cmd_pixel+= ' --project='+params['pixel_classifier_filepath']
        #cmd_pixel+= ' --output_filename_format=' + str(PurePath(dir_, params["output_name"] + "_pixel_probabilities.h5"))
        cmd_pixel+= ' --output_filename_format=' + str(PurePath(tmp_dir, '{nickname}_pixel_probabilities.h5'))
        cmd_pixel+= ' --output_format=hdf5 '
        
        try:
            
            if params["predictions"]:
                cmd_pixel += ' --export_source="simple segmentation"'
            else: raise(KeyError)

        except KeyError:
            cmd_pixel+= ' --export_source="probabilities"'

        cmd_pixel += ' --raw_data ' + " ".join(tmp_file_list)
        subprocess.call(cmd_pixel,shell=True)
    
        for tmp_file in os.listdir(tmp_dir):
            new_file_name = tmp_file.replace(" ","_")

            os.rename(os.path.join(tmp_dir, tmp_file), os.path.join(tmp_dir, new_file_name))
        
        do_pixel = True
    
    else: do_pixel = False

    if 'object_classifier_filepath' in params:
        cmd_object = "/home/bidc/ilastik/run_ilastik.sh --headless"
        cmd_object += ' --project='+params['object_classifier_filepath']
        cmd_object += ' --output_format=hdf5'
        #cmd_object += ' --output_filename_format=' + str(PurePath(dir_, params["output_name"] + "_object_predictions.h5"))
        cmd_object += ' --output_filename_format=' + str(PurePath(tmp_dir, '{nickname}_Object_Prediction.h5'))
        #cmd_object += ' --table_filename=' + str(PurePath(dir_, "object_feature_output.h5"))
        cmd_object += ' --table_filename=' + str(PurePath(tmp_dir,'object_feature_output-{nickname}.csv'))
        cmd_object += ' --export_source="object predictions"'
        cmd_object += ' --readonly'
        cmd_object += ' --raw_data ' + " ".join(tmp_file_list)
        #cmd_object += ' --raw_data ' + str(p)
        if do_pixel:
            cmd_object += ' --prediction_maps ' + " ".join(pixel_probability_maps)
            #cmd_object += ' --prediction_maps ' + str(PurePath(dir_, params['output_name'] + "_pixel_probabilities.h5"))
        subprocess.call(cmd_object,shell=True)

        for f in Path(tmp_dir).glob('*Object*'):
            new_str = str(f).replace(" ","_")
            os.rename(f,new_str)
        do_object = True
    else: do_object = False
 
    stitch(tmp_dir, output_file_base=params['output_name'])
    cleanup(tmp_dir)
