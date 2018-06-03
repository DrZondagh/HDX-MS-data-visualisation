from tkinter import *
from tk import filedialog
import re
import peakutils
#from peakutils.plot import plot as pplot
import matplotlib.pyplot as plt
import os
#import cx_Freeze
import pandas as pd
root = Tk()


intensities = list()
mz = list()
w_inten = list()
peaks = list()
max = list()
mz_peaks = list()
isBi = dict()

def processfiles(fileDirectory):
    for filename in fileDirectory:
        file = open(filename)
        sum = 0
        for line in file.readlines():
            split = line.split(",")
            intensities.append(float(split[1]))
            mz.append(float(split[0]))

        peaks = peakutils.indexes(intensities)
        inten_peak = list()
        for i in peaks:
            inten_peak.append(intensities[i])
        indexes = peakutils.indexes(inten_peak)
        #print(indexes)
        if len(indexes) > 1:
            isBi[filename] = "Yes"
        else:
            isBi[filename] = "No"
        del intensities[:]


#directory = 'PATH'
directory = 'PATH'

a = ['10s-1','20s-1','40s-1','50s-1','60s-2','80s-1','90s-3']
i =0
for fileDirectory in os.listdir(directory):
    try:
        dfs = {}
        fig, ax = plt.subplots(7,1,figsize=(6,12))
        for filename in [directory+fileDirectory+'/'+filename for filename in os.listdir(directory+fileDirectory)]:
            for n in a:
                if n in filename and 'csv' in filename:
                    dfs[n] = (n, pd.read_table(filename, sep=",", names=['Mass(m/z)', 'intensity'], index_col=0))
        for df in dfs:
            n, d = dfs[df]
            d.plot(ax=ax[a.index(n)], legend=None)
        fig.savefig(directory+fileDirectory+'.jpg')
        plt.close("all")
    except NotADirectoryError:
        pass
