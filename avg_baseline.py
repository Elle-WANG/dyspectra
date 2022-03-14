#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:43:24 2022

@author: ywan3191
"""

'''
CASA scripts
average baselines
'''

import numpy as np
import sys


def colored(msg):
    '''make the meesage to red colour
    '''
    return "\033[91m{}\033[0m".format(msg)


# read the ms folder
msname = sys.argv[-1]

# change the save ms name
savename = msname.replace('.ms', '.baseavg.ms')
print(colored('Saving the averaged ms file to {}'.format(savename)))

# open casa table tool
intab = tbtool()
intab.open(msname, nomodify=False)

ant1 = intab.getcol("ANTENNA1")
ant2 = intab.getcol("ANTENNA2")

# Set all antenna pairs equal for baseline averaging
nrows = intab.nrows()
intab.putcol("ANTENNA1", np.zeros(nrows))
intab.putcol("ANTENNA2", np.ones(nrows))

# set an impossible time bin to average (highest time resolution)
interval = intab.getcol("INTERVAL")
timebin = "{}s".format(min(interval) * 1e-2)

uvrange = '>200m'

# average over baselines greater than 200m
mstransform(
    vis=msname,
    outputvis=savename,
    datacolumn="corrected",
    uvrange=uvrange,
    timeaverage=True,
    timebin=timebin,
    keepflags=False,
)

intab.putcol("ANTENNA1", ant1)
intab.putcol("ANTENNA2", ant2)

intab.unlock()
intab.close()

print(colored('Baseline average finished. '))


