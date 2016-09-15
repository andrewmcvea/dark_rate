'''
Calculates the rate of background events (such as muons and 
radioactive background), and plots time vs. charge for these
events to identify what they represent.
To be used with a dataset with no source
'''
import h5py
import numpy as np
from zmq_client import adc_to_voltage

print "start program"

def blech(x):
    something
    return something

if __name__ == '__main__':
    import argparse
    import sys
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='input files')
    args = parser.parse_args()

#Find number of events that occur
    n = len(dset)
    rate = n/t
