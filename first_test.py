# -*- coding: utf-8 -*-
"""
Spyder Editor

Test script for beginning development of online AWAKE event data GUI.

Runs from kernel that exists on my CERN VM on the Technical Network.
"""

#%%

import os
import numpy as np
import cutParser as cp
import time
import h5py
import createNtuple as cn

#%% Set some environment variables

os.environ['AAT'] = '/user/awakeop/AWAKE_ANALYSIS_TOOLS/'

#%% Move to correct directories

os.chdir('/user/awakeop/AWAKE_ANALYSIS_TOOLS')
print(os.getcwd())

#%% Set path to input file

inputFile = '/user/jchappel/scratch/cutSpec_test.txt'
print("\nLoaded Input File with following parameters:\n")
f = open(inputFile)
line = f.readline()
while line:
    print(line)
    line = f.readline()
f.close()

#%% Parse the input cut file and return a list of files within the specified range

InputParsed = cp.inputParser(inputFile)
print(str(len(InputParsed.flist)) + ' events in this time range.')

#%% To test cutting

i = 0
filename_list = InputParsed()[1][1]
for filename in filename_list:
    print(filename)
    a = h5py.File(filename, 'r')
    lsse2_pos = a['AwakeEventData']['LSSE2']['Acq']['position']
    print(lsse2_pos[0])
    i = i + 1

#%% Return a list of files satisfying the cuts

print('Applying cuts...')
start = time.time()
(null, (fb, fl)) = InputParsed()
file_bool = np.array(fb)
file_list = np.array(fl)
use_files = file_list[file_bool]
end = time.time()
print(str(len(use_files)) + ' events passed cuts.')
print('Time Elapsed = ' + str(end - start))

#%% Create the ntuple

start = time.time()
cn.createNtuples(use_files, InputParsed)
end = time.time()
print('Time Elapsed = ' + str(end - start))

