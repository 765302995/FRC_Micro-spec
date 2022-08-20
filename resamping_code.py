#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:SJR
@file:unmannd_spectrum_resamping.py
@mail:2018224033@jou.edu.cn
@func: resamping unmannd spectrum
"""
from scipy.interpolate import PchipInterpolator as PCHIP
import pandas as pd
import numpy as np
import os

def findtxt(path, ret):
    """Finding the *.txt file in specify path"""
    filelist = os.listdir(path)
    for filename in filelist:
        de_path = os.path.join(path, filename)
        if os.path.isfile(de_path):
            if de_path.endswith(".txt"):  # Specify to find the txt file.
                ret.append(de_path)
        else:
            findtxt(de_path, ret)
           
if __name__ == '__main__':

    path = r'F:\projection\2021_unmanned_ship_calibration\20220626_\data\43'
    outpath = os.path.join(path,r're')
    os.mkdir(outpath)
    ret = []
    findtxt(path, ret)
    for j in ret:
        m = os.path.split(j)
        os.chdir(m[0])
        result = pd.DataFrame()
        # path = r'E:\E\sjr\小工具\trios_resampling_spectrum_process\all.txt'
        # data = pd.read_table(j, skiprows=0,names=['wavelength', 'DN'])
        data = pd.read_table(j, skiprows=14,header=None)
        data.fillna(0,inplace=True)
        if data.shape[1] == 2:
            # print(np.ceil(data['wavelength'].min()), np.floor(data['wavelength'].max()))
            newaxis = np.arange(np.ceil(data[0].min()), np.floor(data[0].max()))
            pchip = PCHIP(data[0], data[1])
            y_new = pchip.__call__(newaxis)
            re_wavelength = 're_wavelength'
            re_R_DN='re_R_DN'
            result[re_wavelength] = newaxis
            result[re_R_DN] = y_new
            outputname =outpath+ r'\re_'+m[1]
            result.to_csv(outputname, sep='\t', index=False)
            print('finish{}'.format(j))
        else:
            pass

