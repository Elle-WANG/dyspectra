# dyspectra

make the dynamic spectrum for interested target from model-subtracted ASKAP visibilities 

**Reference:**
https://github.com/joshoewahp/c3369-pipeline

## Reuqirement

* CASA 6.1.0-118
* python-casacore
* numpy
* matplotlib
* astropy
* argparse

## Install

Add your public SSH keys into the github setting (your SSH key for a specific machine can be find:
```
more ~/.ssh/id_rsa.pub
```
Then simply clone the repo
```
git clone git@github.com:Elle-WANG/dyspectra.git
```
You can always use `git pull` to get up-to-date version. 

## Quick Usage

Following the steps:
1. re-center the phase to target position of the visibility file 
2. Average the baseline (exclude short baseline to reduce RFI)
3. Read the telescope correlation data, and calculate the stokes data (and plot)

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
The output vis file (with suffix of `.sourcename.ms`) would save into the same folder of original ms file

### Average baselines 

CASA scripts. Average data over all baselines, with default uv range >200m. 

Example:
```
casa --log2term --nogui -c avg_baseline.py /import/data/scienceData_SB32235_NGC6744.beam12_averaged_cal.J184536.94-645149.ms/
```
The output vis file (with suffix of `.baseavg.ms`) would save into the same folder of original ms file


### Generate and plot dynamic spectrum

Python scripts. Generate several pickle file to save telescope correlation data and stokes data. Plot the dynamic spectrum for each stokes (I, Q, U, V). 

Note the Q, U defination may be different from other conventions. The default setup is `pol_axis=-45`, check `QU calculation` for more details. 

Example:
```
python make_stokes.py /import/data/scienceData_SB28280_EMU_1650-41.beam02_averaged_cal.J164622.64-440533.4.baseavg.ms/
```
The default output files and plots are to save into current directory, you can specify it use `--outdir /import/new/folder/`

To plot imagary part (the default is real part), specify `--imag`

The scripts will automatically calculate the rms level (the standard deviation of imagary component), and plot the cmap in 1 sigma level. You can specify different rms level to generate the plot `--clim 0.2`

The scripts will automatically show the figures during processing. You can use `--noshow` to drop them out. 



## Output files

1. `dyspec_times.pkl`: time series of the observation, unit of `seconds`. Can convert it to human readable format by 

    ```python
    import numpy as np
    from astropy.time import Time
    
    times = np.load("dyspec_times.pkl", allow_pickle=True)
    new_times = Time(times / 24 / 3600, format='mjd', scale='utc')
    new_times.format = 'iso'
    ```
2. `dyspec_freqs.pkl`: frequency series of the observation, unit of `Hz`. 
3. `dyspec_corr_XX.pkl`, `dyspec_corr_XY.pkl`, `dyspec_corr_YX.pkl`, `dyspec_corr_YY.pkl`: telescope correlation data, read from subtracted visibility
4. `dyspec_stokes_I.pkl`, `dyspec_stokes_Q.pkl`, `dyspec_stokes_U.pkl`, `dyspec_stokes_V.pkl`: telescope stokes intensity, calculated from correlation data. Note the default roll axis is -45 deg for ASKAP, but it could be different from different observations. 
5. `dyspec_plot_I.png`, `dyspec_plot_Q.png`, `dyspec_plot_U.png`, `dyspec_plot_V.png`: the dyname spectrum for each stokes


## Other tools 

### Rebin the dynamic spectrum

Python scripts, to bin the dynamic spectrum for any time and frequency resolution. 

Need the outputs from `make_stokes.py` scripts (e.g., `dyspec_stokes_I.pkl`, `dyspec_times.pkl`). 

Example:
```
python rebin_plot.py --tbin 4 --fbin 4
```
The default base folder is the current directory, but you can specify it use `--base /import/data/J164622.64-440533.4/`. The default output folder is the current directory, but you can specify it use '--outdir' as well. 

The `--tbin` and `--fbin` specified the number of bins you want to combined. 

The scripts will automatically save the bined dynamic spectrum, the lightcurve, and the spectrum. 

You can plot the dynamic spectrum from imagary part using `--imag`, but it can only plot real part for the lightcurve and spectrum. 


### QU calculation

Linear polarization depends on the roll axis angle of the telescope, for ASKAP the most common roll axis = -45 deg, which means U is reversed compare to normal CASA calculation. 

This script will give you correct Q/U results based on the roll axis. The roll axis for specific observation can be found in https://apps.atnf.csiro.au/OMP/
* find the specific SBID
* click the SBID and Parset
* find `common.target.src%d.pol_axis = [pa_fixed, 0.0]` (that means pol_axis = 0.0 deg)

Example:
```
python calculate_QU.py 0.0
```




