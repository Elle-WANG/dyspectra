# dyspectra

make the dynamic spectrum from ASKAP visibilities 

**Reference:**
https://github.com/joshoewahp/c3369-pipeline

## Reuqirement

* CASA
* casacore

## Quick Usage


### Recenter the phase

Re-center the phase screen to the target position, mainly depend on https://casadocs.readthedocs.io/en/latest/api/tt/casatasks.manipulation.fixvis.html

The recommend phase center format is _'J052348.6-712552.5'_ (the source name), but the format could be 
* phasecenter = ‘J2000 19h53m50 40d06m00’
* phasecenter = ‘B1950 292.5deg -40.0deg’
* phasecenter = ‘ICRS 13:05:27.2780 -049.28.04.458’
* phasecenter = ‘GALACTIC 47.5rad -60.22rad’

