import numpy as np 
from scipy.signal import butter, lfilter, filtfilt
import matplotlib.pyplot as plt

class signal: 
    
    def __init__(self, signal, s_f=None):
        self.sig= signal 
        self.s_f= s_f
        
    def frequency_range(self):
        """
        Determines a signals frequency range 
        """
        if self.s_f==None:
            raise ValueError('Please Include s_f (samp freq) to get time_range')
            
        N = len(self.sig) # length of the signal
        k = np.arange(N)
        T = N/self.s_f
        return k/T
    def time_range(self):
        """
        Determines a signals time range 
        """
        if self.s_f==None:
            raise ValueError('Please Include s_f (samp freq) to get time_range')
        return np.arange(len(self.sig))/self.s_f

    def fft_plot(self,xlim=None,ylim=None,label=None):
        """
        Generates a FFT or fast fourier transform 
        plot for the input signal.

        Input: Signal, Label (filtered/not), Color of Figure
        Output: Histogram of Frequencies 

        """
        X = np.fft.fft(self.sig)/len(self.sig)
        freqs = self.frequency_range()
        plt.plot(freqs[0:int(len(self.sig)/2)], np.abs(X)[0:int(len(self.sig)/2)],label=label)
        plt.xlabel('Frequency in Hertz [Hz]')
        plt.ylabel('Frequency Domain (Spectrum) Magnitude')
        
        if xlim != None:
            if len(xlim) != 2:
                raise ValueError("xlim && ylim must be tuple or list of coordinates")
            plt.xlim(xlim[0],xlim[1])
        elif ylim != None:
            if len(xlim) != 2:
                raise ValueError("xlim && ylim must be tuple or list of coordinates")
            plt.ylim(ylim[0],ylim[1])
            
        
    def butter_pass(self,filt_type, cutoff,order=5):
        """
        Butterworth lowpass filter:: Allows only signal below 
        certain cutoff to pass through. Order is a constant value
        and is part of the filter arguments. 

        Return b,a inputs for filter 

        """
        nyq = 0.5 * self.s_f
        if filt_type not in ['low','high','band']:
            raise TypeError("filt_type must be of type 'high' or 'low' or 'band'")
        if filt_type == 'band' and len(cutoff) != 2:
            raise ValueError("Bandpass filter needs tuple or list input of min and max freq")
        if filt_type == 'band':
            low = cutoff[0] / nyq
            high = cutoff[1] / nyq
            b, a = butter(order, [low, high], btype='band')
        else:   
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype=filt_type, analog=False)
            
        return b, a

    def butter_filter(self,filt_type,cutoff,order=5):
        """
        Low pass filter for the signal data w/r to a particular
        cut off frequency. 
        """
        b, a = self.butter_pass(filt_type,cutoff, order)
        if filt_type == 'low' or 'band':
            return lfilter(b, a, self.sig)
        elif filt_type == 'high':
            return filtfilt(b, a, self.sig)
    


##############################
if __name__ == '__main__': 
    s_f=1000 #samps/sec
    T=1/s_f
    time = np.arange(0,.5,T)

    sample_sig = np.sin(40 * 2 * np.pi * time) + .5*np.sin(90 * 2 * np.pi * time)

    plt.figure(figsize=(60,20))
    plt.suptitle('Examination of Signal Isolation and Construction')
    plt.subplot(231)
    y_1= np.sin(40 * 2 * np.pi * time)
    plt.plot(time,y_1,color='b')

    plt.xlabel("time [s]")
    plt.title("Function 1: sin(80πt)")
    plt.subplot(232)
    y_2 = .5*np.sin(90 * 2 * np.pi * time)
    plt.plot(time,y_2,color='r')

    plt.xlabel("time [s]")
    plt.title("Function 2: .5*sin(180πt)")
    plt.subplot(233)
    plt.title("Function 1 + Function 2: {}".format('sin(80πt)+.5*sin(180πt)'))
    plt.plot(time,y_1,color='b',label='function1')
    plt.plot(time,y_2,color='r',label='function2')
    plt.xlabel("time [s]")
    plt.legend(loc='upper right')
  

    ####signal processing

    f=signal(signal= sample_sig, s_f=s_f)
    lowpass= f.butter_filter(filt_type='low', cutoff=80)
    highpass= f.butter_filter(filt_type='high', cutoff=80)

    
    plt.subplot(234)
    f.fft_plot()
    plt.subplot(235)
    signal(lowpass,f.s_f).fft_plot(label='low_pass')
    signal(highpass,f.s_f).fft_plot(label='high_pass')
    plt.legend()
    plt.show()



    # time = np.arange(0,.5,1/1000)  
    # sample_sig = np.sin(40 * 2 * np.pi * time) + 0.5 * np.sin(90 * 2 * np.pi * time)

    # f=signal(signal= sample_sig, s_f=1000)
    # lowpass= f.butter_filter(filt_type='low', cutoff=80)
    # highpass= f.butter_filter(filt_type='high', cutoff=80)
    # bandpass= f.butter_filter(filt_type='band', cutoff=[30,90])

    # plt.figure(figsize=(20,4))
    # plt.subplot(121)
    # f.fft_plot()
    # plt.subplot(122)
    # signal(lowpass,f.s_f).fft_plot(label='low_pass')
    # signal(highpass,f.s_f).fft_plot(label='high_pass')

    # plt.legend()
    # plt.show()
    # signal(bandpass,f.s_f).fft_plot(label='band_pass')