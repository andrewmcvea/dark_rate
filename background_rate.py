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

print "start program"

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='input files')
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
    n = len(dset)
    print "Number of Events=",n

    rate = n/td
    print "Background Rate=", rate
