# dyspectra

make the dynamic spectrum from ASKAP visibilities 

**Reference:**
https://github.com/joshoewahp/c3369-pipeline

## Reuqirement

* CASA 5.1.2
* casacore

## Quick Usage

Following the steps:
1. re-center the phase to target position of the visibility file 
2. Average the baseline (exclude short baseline to reduce RFI)

### Recenter the phase

Re-center the phase screen to the target position, mainly depend on https://casadocs.readthedocs.io/en/latest/api/tt/casatasks.manipulation.fixvis.html

The recommend phase center format is `J052348.6-712552.5` (the source name), but the format could be 
* phasecenter = `'J2000 19h53m50 40d06m00'`
* phasecenter = 'B1950 292.5deg -40.0deg'
* phasecenter = 'ICRS 13:05:27.2780 -049.28.04.458'
* phasecenter = 'GALACTIC 47.5rad -60.22rad'

Example:
```
casa --log2term --nogui -c recenter_phase.py /import/data/scienceData_SB32235_NGC6744.beam12_averaged_cal.ms/ J184536.94-645149.55
```
The output vis file would save into the same folder of original ms file

### Average baselines 

CASA scripts. Average data over all baselines, with default uv range >200m. 

Example:
```
casa --log2term --nogui -c avg_baseline.py /import/data/scienceData_SB32235_NGC6744.beam12_averaged_cal.J184536.94-645149.ms/
```
The output vis file would save into the same folder of original ms file

### QU calculation

Linear polarization depends on the roll axis angle of the telescope, for ASKAP the most common roll axis = -45 deg, which means U is reversed compare to normal CASA calculation. 

This script will give you correct Q/U results based on the roll axis. 

Example:
```
python calculate_QU.py -45
```




