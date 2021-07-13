import numpy as np
from scipy import signal
fname = '../data/motor_imagery.npz'

alldat = np.load(fname, allow_pickle=True)['dat']
dat1 = alldat[0][0] #only used to reference shape

def pre_process(subj, exp, hpf=None):
    """quick way to get broadband power in time-varying windows"""
    # pick subject 0 and experiment 0 (real movements)
    dat1 = alldat[subj][exp]

    # V is the voltage data
    V = dat1['V'].astype('float32')
    
    if hpf:
        # high-pass filter above 50 Hz
        b, a = signal.butter(3, [hpf], btype = 'high', fs=1000) # why is it a thrid order filter?
        V = signal.filtfilt(b,a,V,0)

        # compute smooth envelope of this signal = approx power
        V = np.abs(V)**2
        b, a = signal.butter(3, [10], btype = 'low', fs=1000)
        V = signal.filtfilt(b,a,V,0)

        # normalize each channel so its mean power is 1
        V = V/V.mean(0) 
    return V

def comp_avg_signal(V, length, muscle):
    """average the broadband power across all tongue and hand trials"""
    nt, nchan = V.shape
    nstim = len(dat1['t_on'])
    stim_id = {'tongue':11, 'hand':12}[muscle]
    trange = np.arange(0, length) #time range?
    ts = dat1['t_on'][:,np.newaxis] + trange #time series 
    V_epochs = np.reshape(V[ts, :], (nstim, length, nchan))
    return (V_epochs[dat1['stim_id']==stim_id]).mean(0) # averging across the experiment no.


#### TODO: LOAD DATA ACROSS SUBJECTS ###
# all_psds = {'overt':[], 'imag':[]}
# for s in range(7):
#     try:
#         nonfilter_overt = pre_process(subj=s, exp=0)
#         nonfilter_imag = pre_process(subj=s, exp=1)

#         sample_overt = comp_avg_signal(nonfilter_overt, 9960, 'hand')
#         sample_imag = comp_avg_signal(nonfilter_imag, 9960, 'hand')

#         signals = {'overt': sample_overt, 'imag': sample_imag}
#         psds = {'overt' : [], 'imag' : [] }

#         for chan in range(46):
#             for k in psds.keys():
#                 freqs, powers = compute_spectrum(signals[k][:,chan], **kwargs)
#                 psds[k].append(powers)
#         for k in psds.keys():
#             psds[k] = np.array(psds[k])
#             all_psds[k].append(psds[k])
#     except:
#         print(s)
        
# for k in all_psds.keys():
#     all_psds[k] = np.array(all_psds[k]).mean(0)
### END TODO ###