#Calculates the dark rate of the PMTs
import h5py
import numpy as np
import matplotlib.pyplot as plt

print "start program"

#Finds the amplitude of each of the charge curves with barrier
def find_amp(v):
        amplitude = np.min(v,axis=1)
        #vamp = adc_to_voltage(amplitude)
        mask = amplitude < -20
        filteramp = amplitude[mask]
        return abs(filteramp)
'''
Finds the timing window to calculate dark rate by placing a
threshold voltage higher than the dark pulses that once
surpassed marks the end of the window
'''
def find_window(x):
    amps = find_amp(x)
    threshold = amps > 100
    famps = amps[theshold]
    times = famps.time
    window = np.min(times)
    return window

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

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='input files')
        parser.add_argument('-c', '--chunk', type=int, default=10000)
    args = parser.parse_args()

    t = []
    for filename in args.filenames:
        with h5py.File(filename) as f:
            for i in range(0, f['c1'].shape[0], args.chunk):
                y1 = f['c1'][i:i+args.chunk]
                mask = np.min(y1,axis=-1) < -100
                y1 = y1[mask]
                t1 = get_times(y1)
                t.extend(t1)

    window = np.min(t)

    amp = []
    for filename in args.filenames:
        with h5py.File(filename) as f:
            dset = f['c1'][:100000]
            '''
            filter dataset to only be those
            that correspond to values of
            t < window
            '''
            amp1 = find_amp(dset)
            amp.extend(amp1)

    np = len(amp)
    ne = len(t)

    dr = np/(window-ne)

    print "Time=",window
    print "Pulses=",np
    print "Events=",ne
    print "Dark Rate=",dr

    for filename in args.filenames:
        with h5py.File(filename) as f:
            for i in range(1):
                plt.plot(f['c1'][i])
            plt.title('channel 1')

    plt.plot((window,window), (250,-2500), 'k-')

plt.show()
