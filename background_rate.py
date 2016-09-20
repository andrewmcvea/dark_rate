'''
Calculates the rate of background events (such as muons and
radioactive background), and plots time vs. charge for these
events to identify what they represent.
To be used with a dataset with no source
'''

import h5py
import numpy as np
from zmq_client import adc_to_voltage
import os.path, time
import matplotlib.pyplot as plt
import heapq

print "start program"

#Courtesy of Hadar and Tony's newbar.py
def get_window(v):
    ind = np.argmin(v[np.min(v,axis=1) < -10],axis=1)
    med = np.median(ind)
    # 20 ns window
    return med - 20, med + 20

def get_times(y, fraction=0.4):
    """ 
    Returns pulse times in `y` by looking for the pulse
    to cross a constant fraction `fraction` of the pulse height in each
    waveform. `y` should be a 2 dimensional array with shape (N,M) where
    N is the number of waveforms, and M is the number of samples per
    waveform.
    """ 
    # samples below threshold
    mask1 = y > np.min(y,axis=-1)[:,np.newaxis]*fraction
    # samples before the minimum
    mask2 = np.arange(y.shape[1]) < np.argmin(y,axis=-1)[:,np.newaxis]

    # right side of threshold crossing
    r = y.shape[1] - np.argmax((mask1 & mask2)[:,::-1], axis=-1)
    r[r == 0] = 1
    r[r == y.shape[1]] = y.shape[1] - 1
    l = r - 1

    yl = y[np.arange(y.shape[0]),l]
    yr = y[np.arange(y.shape[0]),r]

    return (np.min(y,axis=-1)*fraction - yl)/(yr-yl) + l
    
if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='input files')
    parser.add_argument('-c', '--chunk', type=int, default=10000)
    args = parser.parse_args()

    '''
    To find the time to collect one data set input to two data sets
    taken in succession and subtract the creation time of the second
    from the first. Thus the second dataset is the one being analyzed
    '''

    g = args.filenames[0]
    h = args.filenames[1]

    t2 = os.path.getmtime(g)
    t1 = os.path.getmtime(h)
    td = abs(t2 - t1) #Find the amount of time it took to take the data
    print "Time=", td

    f = h5py.File(h)
    dset = f['c2'][:100000]
    win = get_window(dset)
    charge = -adc_to_voltage(np.trapz(dset[:,win[0]:win[1]]))*1e3/2/50.0

    t = []
    for i in range(0, f['c1'].shape[0], args.chunk):
        y1 = adc_to_voltage(f['c1'][i:i+args.chunk])
        y2 = adc_to_voltage(f['c2'][i:i+args.chunk])
        #only accept c2 events below -10 mV
        mask = np.min(y2,axis=-1) < -10e-3
        #tony's new line
        mask &= np.min(y1, axis=-1) < -100e-3
        y1 = y1[mask]
        y2 = y2[mask]
        t1 = get_times(y1)*0.5 # sample -> ns
        t2 = get_times(y2)*0.5
        res = t2 - t1
        t.extend(res)
        
    n = len(dset)
    print "Number of Events=",n

    rate = n/td
    print "Background Rate=", rate
    
    charge = heapq.nlargest(len(t), charge)

    plt.plot(t, charge, 'ro')
    plt.ylabel("Charge(pC)")
    plt.xlabel("Time(ns)")
    plt.title("Charge vs. Time")

plt.show()
