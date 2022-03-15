#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:24:58 2022

@author: ywan3191
"""


'''
check what's the proper stokes Q and U based on roll axis angle
'''

import sys
import numpy as np

# most fo RACS survey has a roll axis angle = -45 deg
pol_axis = np.radians(float(sys.argv[-1]))
theta = 2.0 * pol_axis

def colored(msg):
    '''make the meesage to red colour
    '''
    return "\033[91m{}\033[0m".format(msg)

print(colored('The most commone pol axis = -45 deg (e.g., RACS) \n'
              'Check the exact pol axis in OMP https://apps.atnf.csiro.au/OMP \n' 
              'Find the SBID and check the Parset, \n'
              'to see "common.target.src1.pol_axis = [pa_fixed, -45.0]"' 
              '\n==============\n'))

print("pol_axis=%.1f deg" %(np.degrees(pol_axis)))
print("Q=[%.3f*(XY+YX) %.3f*(XX-YY)]" %(np.cos(theta),- np.sin(theta)))
print("U=[%.3f*(XY+YX) %.3f*(XX-YY)]\n" %(np.sin(theta), np.cos(theta)))

