#!/bin/bash
#### bash ~/scripts/dyspectra/run_dyspec.sh target.ms J183807.40-075604.71

msname=$1               # without .ms
phasecen=$2             # in format of Jxxxxxx.xx+xxxxxx.xx
echo $msname $phasecen

loc=$(dirname "$0")     # location of scripts 
msname=${msname::-3}    # cut .ms affix 
echo $loc $msname
echo 

mkdir dyspec

recenter_phase="casa --log2term --nogui -c $loc/recenter_phase_casa6.py $msname.ms $phasecen"
avg_baseline="casa --log2term --nogui -c $loc/avg_baseline.py $msname.$phasecen.ms"
#make_stokes="python $loc/make_stokes.py $msname.$phasecen.baseavg.ms --noshow --columnname CORRECTED_DATA --outdir dyspec"
make_stokes="python $loc/make_stokes.py $msname.$phasecen.baseavg.ms --noshow --columnname DATA --outdir dyspec"

echo $recenter_phase
echo $avg_baseline
echo $make_stokes
echo

$recenter_phase

$avg_baseline

$make_stokes

