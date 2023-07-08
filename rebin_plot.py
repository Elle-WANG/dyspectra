#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 16:02:26 2022

@author: ywan3191
"""

'''
Rebin the resolution for dynamic spectrum; 
Make lightcurve (in any resolution); 
Make spectrum (in any resolution); 
'''

import os
import numpy as np
import sys

import make_stokes 
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from astropy.time import Time



def _main():
    parser = argparse.ArgumentParser(description='Get the stokes intensity, and plot', 
                                      formatter_class=argparse.HelpFormatter)
    # parser.add_argument('ms', type=str, 
    #                     help='Input measurement set (baseline averaged)')
    parser.add_argument('--outdir', type=str, default='.', 
                        help='Specify the directory to save data and plots')
    parser.add_argument('--base', type=str, default='.', help='Folder to store the XX, YY data')
    parser.add_argument('--stokes', type=str, choices=['I', 'Q', 'U', 'V'], 
                        default='I', help='which stokes to plot, I, Q, U, V')
    parser.add_argument('--tbin', type=int, default=1, help='Number of folded bin in time axis')
    parser.add_argument('--fbin', type=int, default=1, help='Number of folded bin in freq axis')
    parser.add_argument('--noflag', action='store_true', help='Without flagging data')
    parser.add_argument('--imag', action='store_true', help='Plot imagary part')
    parser.add_argument('--clim', type=float, default=1.0, help='Cmap rms level')
    parser.add_argument('--noshow', action='store_true', help='Do not show the plot')
    
    values = parser.parse_args()
    
    if values.noshow:
        matplotlib.use('Agg')
        
    # create saving directory
    if not os.path.exists(values.outdir):
        print(colored('Creating new folder {}...'.format(values.outdir)))
        os.mkdir(values.outdir)
    else:
        print(colored('Saving to current folder {}...'.format(values.outdir)))
        
    # read the data
    folder = values.base
    try: 
        times = np.load(os.path.join(folder, 'dyspec_times.pkl'), allow_pickle=True)
        freqs = np.load(os.path.join(folder, 'dyspec_freqs.pkl'), allow_pickle=True)
        data = np.load(os.path.join(folder, 'dyspec_stokes_{}.pkl'.format(values.stokes)), 
                       allow_pickle=True)
    except:
        print('ERROR: we want the output from make_stokes.py')
        sys.exit()
        
    # bined data
    data = databin_2d(data, values.tbin, values.fbin)
    times = databin_1d(times, values.tbin)
    freqs = databin_1d(freqs, values.fbin)
    
    # savename
    savename = 'plot_{}_tbin{}_fbin{}.png'.format(values.stokes, values.tbin, values.fbin)
    if values.imag:
        savename = savename[:-4] + "_imag" + savename[-4:]

    # plot dynamic spectrum 
    make_stokes.plot_dyspec(data, times, freqs, values.stokes, values, os.path.join(values.outdir, 'dyspec_'+savename))

    # plot lightcurve
    if not values.imag:
        plot_lightcurve(np.real(data)*1e3, times, values, os.path.join(values.outdir, 'lc_'+savename))
    else:
        plot_lightcurve(np.imag(data)*1e3, times, values, os.path.join(values.outdir, 'lc_'+savename))

    # plot spectrum
    if not values.imag:
        plot_spectrum(np.real(data)*1e3, freqs/1e6, values, os.path.join(values.outdir, 'sp_'+savename))
    else:
        plot_spectrum(np.imag(data)*1e3, freqs/1e6, values, os.path.join(values.outdir, 'sp_'+savename))

    print(colored('INFO: Plotting finished. '))


def colored(msg):
    '''make the meesage to red colour
    '''
    return "\033[91m{}\033[0m".format(msg)


def databin_2d(data, tfold, ffold):
    # data bin in 2D
    data = np.nanmean(data[:int(data.shape[0]/tfold)*tfold].reshape(-1, tfold, data.shape[1]), axis=1)
    data = np.nanmean(data[:, :int(data.shape[1]/ffold)*ffold].reshape(data.shape[0], -1, ffold), axis=2)
    return data 


def databin_1d(data, fold):
    # data bin in 1D 
    data = np.nanmean(data[:int(data.shape[0]/fold)*fold].reshape(-1, fold), axis=1)
    return data


def plot_lightcurve(data, times, values, savename):
    
    fig, ax = plt.subplots(figsize=(8, 6))

    time_length = (times[-1] - times[0]) / 3600 # unit of hours
    times = Time(times / 24 / 3600, format='mjd', scale='utc')
    times.format = 'datetime64'
    
    ax.plot(times.value, np.nanmean(data, axis=1), color='black', marker='.', alpha=0.6)
    
    date_form = mdates.DateFormatter("%Y-%b-%d/%H:%M")
    ax.xaxis.set_major_formatter(date_form)
    
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Flux Density (mJy/beam)')
    ax.set_title('Stokes {}'.format(values.stokes))
    
    # set a reasonable time interval
    if int(time_length/4) != 0:
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=int(time_length/4)))

    fig.autofmt_xdate(rotation=15)
    
    fig.savefig(savename, dpi=300, bbox_inches='tight')
    
    if not values.noshow:
        plt.show()
    else:
        plt.close()
        
        
def plot_spectrum(data, freqs, values, savename):
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(freqs, np.nanmean(data, axis=0), color='black')
    
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Flux Density (mJy/beam)')
    ax.set_title('Stokes {}'.format(values.stokes))
    
    fig.savefig(savename, dpi=300, bbox_inches='tight')
    
    if not values.noshow:
        plt.show()
    else:
        plt.close()
        


if __name__ == "__main__":
    _main()

