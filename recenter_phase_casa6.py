#!/usr/bin/env python

"""
Created on Mon Mar 14 15:56:59 2022

@author: ywan3191
"""

'''
a CASA script
change the phase center
'''

import sys


def colored(msg):
    '''make the meesage to red colour
    '''
    return "\033[91m{}\033[0m".format(msg)



def formated(phasecen):
    '''formated the phase center - from Jxxxx+xxxx to standard CASA format
    '''
    if '-' in phasecen:
        a = phasecen[1:].split('-')
        a.append('-')
    elif '+' in phasecen:
        a = phasecen[1:].split('+')
        a.append('+')
    
    return 'J2000 {}h{}m{} {}{}d{}m{}'.format(a[0][:2], a[0][2:4], a[0][4:], 
                                              a[2], 
                                              a[1][:2], a[1][2:4], a[1][4:])



# input measurement and phase center (target coordinates)
msname = sys.argv[-2]
phasecen = sys.argv[-1]


# convert format of phasecen
if ' ' not in phasecen:
    phase_coord = formated(phasecen)
    print(colored('Convert {} to {}'.format(phasecen, phase_coord)))
else:
    phase_coord = phasecen


# new output recentred vis
rotated_ms = msname.replace('.ms', '.'+phasecen.replace(' ', '_')+'.ms')
print(colored('Write rotated ms file to {}'.format(rotated_ms)))

# rotate!
phaseshift(vis=msname, outputvis=rotated_ms, phasecenter=phase_coord)


