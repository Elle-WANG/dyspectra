#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 21:44:19 2022

@author: ywan3191
"""

'''
python scripts
Make the dynamic spectrum from reading the ms data directly 
'''


import os
import argparse
import numpy as np
from casacore.tables import table
from astropy.time import Time

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib



def _main():
    parser = argparse.ArgumentParser(description='Get the stokes intensity, and plot', 
                                     formatter_class=argparse.HelpFormatter)
    parser.add_argument('ms', type=str, 
                        help='Input measurement set (baseline averaged)')
    parser.add_argument('--outdir', type=str, default='.', 
                        help='Specify the directory to save data and plots')
    parser.add_argument('--columnname', type=str, default='DATA', 
                        help='The columnname to plot the data, DATA or CORRECTED_DATA, ' 
                        "normally there's only DATA column for baseline averaged data. ")
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

    # read the visibility table
    t = table(values.ms)
    
    # get antenna correlation
    corr_list = get_corr(t, values)
    print(colored('Get the antenna correlation, XX, XY, YX, YY...'))
    
    # get the stokes intensity 
    I, Q, U, V = get_stokes(corr_list, values)
    print(colored('Get the full stokes I, Q, U, V... '))
    
    # get the time arrays
    times = np.unique(t.getcol("TIME"))
    freqs = table(os.path.join(values.ms, 'SPECTRAL_WINDOW'))[0]['CHAN_FREQ']
    times.dump(os.path.join(values.outdir, 'dyspec_times.pkl'))
    freqs.dump(os.path.join(values.outdir, 'dyspec_freqs.pkl'))
    print(colored('Get time and frequency data array...'))
    
    # plot the figure
    plot_dyspec(I, times, freqs, 'I', values)
    plot_dyspec(Q, times, freqs, 'Q', values)
    plot_dyspec(U, times, freqs, 'U', values)
    plot_dyspec(V, times, freqs, 'V', values)
    
    print(colored('Plot finished. '))
    
    
    
    
def plot_dyspec(poldata, times, freqs, pol, values):
    '''Plot 2D dynamic spectrum for specific stokes
    '''
    
    poldata = poldata * 1e3 # unit of mJy
    
    # get the rms level from the imagary part
    rms = np.std(np.imag(poldata))
    print(colored('RMS LEVEL: {:.2f} mJy for stokes {}'.format(rms, pol)))
    
    if values.imag:
        print(colored('Plot imagary part ...'))
        data = np.imag(poldata).transpose()
    else:
        data = np.real(poldata).transpose()
    
    # times, freqs
    time_length = (times[-1] - times[0]) / 3600 # unit of hours
    times = Time(times / 24 / 3600, format='mjd', scale='utc')
    times.format = 'datetime64'
    
    tmin, tmax = mdates.date2num(times[0].value), mdates.date2num(times[-1].value)
    
    freqs = freqs / 1e6 # unit of MHz
    fmin, fmax = np.min(freqs), np.max(freqs)
    
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(data, origin='lower', 
                    extent=[tmin, tmax, fmin, fmax], 
                    aspect='auto', cmap='inferno', 
                    clim=(-values.clim*rms, values.clim*rms))
    
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.02)
    
    date_form = mdates.DateFormatter("%Y-%b-%d/%H:%M")
    ax.xaxis.set_major_formatter(date_form)

    # set a reasonable time interval
    if int(time_length/4) != 0:
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=int(time_length/4)))

    fig.autofmt_xdate(rotation=15)
    
    ax.set_title('Stokes {}'.format(pol))
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Frequency (MHz)')
    cb.set_label('Flux Density (mJy/beam)')
    
    savename = os.path.join(values.outdir, 'dyspec_plot_{}.png'.format(pol))
    fig.savefig(savename, dpi=300, bbox_inches='tight')
    
    if not values.noshow:
        plt.show()
    else:
        plt.close()




def get_stokes(corr_list, values):
    '''Get the full stokes intensity, I, Q, U, V
    Note the ASKAP defination may different from others
    '''
    # convert those correlation to stokes
    # note we always assume roll aixs = -45 deg here
    XX, XY, YX, YY = corr_list[0], corr_list[1], corr_list[2], corr_list[3]
    
    I = (XX + YY) / 2
    Q = (XX - YY) / 2
    U = - (XY + YX) / 2
    V = 1j * (XY - YX) / 2
    
    # save the data
    I.dump(os.path.join(values.outdir, 'dyspec_stokes_{}.pkl'.format('I')))
    Q.dump(os.path.join(values.outdir, 'dyspec_stokes_{}.pkl'.format('Q')))
    U.dump(os.path.join(values.outdir, 'dyspec_stokes_{}.pkl'.format('U')))
    V.dump(os.path.join(values.outdir, 'dyspec_stokes_{}.pkl'.format('V')))
    
    return I, Q, U, V
    



def get_corr(t, values):
    '''
    Get the antenna correlation from visibility; 
    Save the data array to pickle
    '''
    pols = ['XX', 'XY', 'YX', 'YY']
    corr_list = []
    
    for polidx, pol in enumerate(pols):
        corr = t.getcol(values.columnname)[:, :, polidx]
    
        # mask flagged data
        if not values.noflag:
            vis_flag = t.getcol("FLAG")[:, :, polidx]
            corr = np.ma.masked_where(vis_flag, corr)
            
        # save data
        savename = os.path.join(values.outdir, 'dyspec_corr_{}.pkl'.format(pol))
        corr.dump(savename)
        
        # save it into list
        corr_list.append(corr)
        
    return corr_list



def colored(msg):
    '''make the meesage to red colour
    '''
    return "\033[91m{}\033[0m".format(msg)




if __name__ == "__main__":
    _main()

