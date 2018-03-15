# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:00:39 2018

@author: Austin Mackillop

YIN Algorithm
"""
from api.capstoneModules.audioFunctions import recordToFile, getData, butterLowpassFilter, downSample, trim
#from scipy.signal import correlate
#from matplotlib.pyplot import plot, figure, close
from numpy import mean, correlate, asarray, zeros, polyfit, poly1d, float32, int32
from numpy import sum as npsum


def crossCorr(x, tau, W, auto = False):
    """
    Autocorrelation, Step 1, Eq. (1)\n
    
    Computes the cross correlation between a signal and a shifted version. If auto = True, 
    computes the auto correlation of the signal shifted by tau.
    
    # Arguments
        x: A 1-D numpy array containing the signal\n
        tau: Integer sample lag
        W: Integer integration window size.
        auto: Boolean, set True for autocorrelation
        
    # Returns
        cross_corr_mat: A 2-D numpy array of the correlation function for each sample. 
        Each row corresponds to a sample.
    """
        
    cross_corr_mat = zeros((x.size//W, W), float32)
    x_orig = list(x)
    for i in range(cross_corr_mat.shape[0]):
        t = i*W
        # Unbias the signals
        x = x_orig[t:W+t] - mean(x_orig[t:W+t])
        x_tau = x_orig[t+tau:t+tau+W] - mean(x_orig[t+tau:t+tau+W])
        if (auto == False):
            cross_corr = correlate(x, x_tau, 'full')#/npsum(x**2)
            cross_corr_mat[i,:] = cross_corr[cross_corr.shape[0]//2:]
        else:
            cross_corr = correlate(x_tau, x_tau, 'full')
            cross_corr_mat[i,:] = cross_corr[cross_corr.shape[0]//2:]
    return cross_corr_mat


def diffEquation(x, W):
    """
    Difference Equation, Step 2, Eq. (7)\n
    
    Computes the difference equation for each sample
    
    # Arguments
        x: A 1-D numpy array containing the signal\n
        W: Integration window size
        
    # Returns
        diff_eq_mat: A 2-D numpy array of the computed difference equations for each sample.
        Each row corresponds to a sample.
    """
    
#    cross_corr_lag = crossCorr(x, 0, W, auto = True)
#    if not tau%2:
    auto_corr_mat = crossCorr(x, 0, W, auto = True)
    diff_eq_mat = zeros(auto_corr_mat.shape, float32)
    for i in range(0, diff_eq_mat.shape[0]):
        diff_eq_mat[i,:] = auto_corr_mat[i, 0] + crossCorr(x, i, W, auto = True)[i, 0] - 2 * auto_corr_mat[i,:]
    return diff_eq_mat

def cumMeanNormDiffEq(x, W):
    """
    Cumulative Mean Normal Difference Equation, Step 3, Eq. (8)\n
    
    Computes the cumulative mean normal difference equation for each sample
    
    # Arguments
        x: A 1-D numpy array containing the signal\n
        W: Integration window size
        
    # Returns
        cum_diff_mat: A 2-D numpy array of the computed difference equations
        for each sample. Each row corresponds to a sample.
    """
    diff_eq_mat = diffEquation(x, W)
    cum_diff_mat = zeros(diff_eq_mat.shape, float32)
    cum_diff_mat[:, 0] = 1
    for t in range(diff_eq_mat.shape[0]):
        for j in range(1, diff_eq_mat.shape[1]):
            cum_diff_mat[t, j] = diff_eq_mat[t, j]/((1/j)*npsum(diff_eq_mat[t, 1:j+1]))
    return cum_diff_mat
        
def absoluteThresold(x, freq_range = (40, 300), threshold = 0.1, Fs = 16e3):
    """
    Absolute Threshold Method, Step 4\n
    
    Computes the initial period predicition of each sample using the method described
    in Step 4 of the paper.
    
    #Arguments
        x: A 1-D numpy array containging the signal\n
        freq-range: A tuple containing the search range ex. (min_freq, max_freq)\n
        threshold: A floating point threshold value for picking the minimum of the
        cumulative mean normal difference equation.\n
        Fs: The sampling rate.
    
    #Returns
        taus: A 1-D numpy array containing the candidate period estimates for each sample.\n
        cum_diff_mat: A 2-D numpy array, see documentaion for `cumMeanNormDiffEq`.
    
    #Raises
        Not handed yet.
    """
    tau_min = int(Fs)//freq_range[1]
    tau_max = int(Fs)//freq_range[0]

    taus = zeros(x.size//tau_max, int32)
    tau_star = 0
    minimum = 1e9
    cum_diff_mat = cumMeanNormDiffEq(x, tau_max)
    for i in range(x.size//tau_max):
        cum_diff_eq = cum_diff_mat[i,:]
        for tau in range(tau_min, tau_max):
            if cum_diff_eq[tau] < threshold:
                taus[i] = tau
                break
            elif cum_diff_eq[tau] < minimum:
                tau_star = tau
                minimum = cum_diff_eq[tau]
        if taus[i] == 0:
            taus[i] = tau_star
    return taus, cum_diff_mat
    
def parabolicInterpolation(cum_diff_matrix, taus, freq_range, Fs):
    """
    Parabolic Interpolation, Step 4\n
    
    Applies parabolic interpolation onto the candidate period estimates using
    3 points corresponding to the estimate and it's adjacent values
    
    #Arguments
        cum_diff_matrix: A 2-D numpy array, see documentaion for `cumMeanNormDiffEq`\n
        taus: A 1-D numpy array for the candidate estimates
        freq-range: A tuple containing the search range ex. (min_freq, max_freq)\n
        Fs: The sampling rate.
    
    #Returns
        local_min_abscissae: A 1-D numpy array containing the interpolated period estimates
        for each sample.
    
    #Raises
        Not handed yet.
    """
    abscissae = zeros((len(taus)-2, 3), float32)
    ordinates = zeros(abscissae.shape, float32)
    #if taus == []:
    for i, tau in enumerate(taus[1:-1]):
        ordinates[i-1] = cum_diff_matrix[i, tau-1:tau+2]
        abscissae[i-1] = asarray([tau-1, tau, tau+1], float32)
        
    period_min = int(Fs)//freq_range[1]
    period_max = int(Fs)//freq_range[0]
        
    coeffs = zeros((len(taus)-2, 3))
    local_min_abscissae = zeros(coeffs.shape[0])
    local_min_ordinates = zeros(coeffs.shape[0])
    for i in range(0, len(taus)-2):
        coeffs[i] = polyfit(abscissae[i,:], ordinates[i,:], 2)
        p = poly1d(coeffs[i]).deriv()
        if p.roots > period_min and p.roots < period_max:
            local_min_abscissae[i] = p.roots
        else:
            local_min_abscissae[i] = taus[i+1]
        local_min_ordinates[i] = p(local_min_abscissae[i])
        
    return local_min_abscissae

def pitchTrackingYIN(fname, freq_range = (40, 300), threshold = 0.1, timestep = 0.1, Fs = 48e3, target_Fs = 8e3, Fc = 1e3, down_sample = False):
#    fname = "C:/Users/Austin/Desktop/School/Capstone/Speechbuddy-master/src/demo.wav"
#    freq_range = (40, 300)
#    threshold = 0.1
#    timestep = 0.25
#    Fs = 16e3
#    Fc = 1e3
#    down_sample = False

    signal = getData(fname)
    step = int(Fs//target_Fs)
    signal = downSample(signal, 1e3, Fs, step)
    Fs = int(target_Fs)
    signal = butterLowpassFilter(signal, Fc, Fs, 6)
    signal = asarray(trim(signal))
    #signal = signal/max(signal)
    signal = signal.astype(float32)
    W = int(Fs)//freq_range[0]
    sampled_signal = zeros(((signal.size//int(Fs*timestep)),2*W+2), float32)
    for i in range((signal.size//int(Fs*timestep))):
        t = int(i*Fs*timestep)
        sampled_signal[i,:] = signal[t:int(t+2*W+2)]/max(signal[t:int(t+2*W+2)])
        
    sampled_signal = sampled_signal.flatten()
    signal = sampled_signal
    taus = absoluteThresold(signal, freq_range, threshold, Fs)[0]
    diff_mat = diffEquation(signal, W)
    periods = parabolicInterpolation(diff_mat, taus, freq_range, Fs)
    

    f0 = zeros((signal.size//W-2, 2), int32)
    for i in range(signal.size//W-2):
        f0[i,0] = i
        f0[i,1] = Fs//periods[i]
#    print("AVerage:   ", mean(f0), "    Time:   ", time()-time_start)
#    figure()
#    plot(f0)
    return f0
"""
Cumulative Mean Normalized Difference Function, Eq. (8)
"""
#fname = "../audio/output.wav"
##signal = getData(fname)
##signal = trim
#f0 = pitchTrackingYIN(fname)

#plot(signal)

